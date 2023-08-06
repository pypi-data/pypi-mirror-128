from __future__ import annotations

import enum
import os
from typing import TYPE_CHECKING, Any, Awaitable, Dict, Optional, Tuple, Union, cast
import uuid

from google.protobuf.timestamp_pb2 import Timestamp
import grpc
import jsonpickle

from jetpack import __version__
from jetpack._job.future import Future
from jetpack._remote import codec
from jetpack.config import namespace
from jetpack.proto.runtime.v1alpha1 import remote_pb2, remote_pb2_grpc

# Prevent circular dependency
if TYPE_CHECKING:
    from jetpack._job.job import Job


@enum.unique
class LaunchJobMode(enum.Enum):
    ASYNC = "ASYNC"
    ASYNC_FIRE_AND_FORGET = "ASYNC_FIRE_AND_FORGET"
    FIRE_AND_FORGET = "FIRE_AND_FORGET"
    BLOCKING = "BLOCKING"


def mode_is_async(mode: LaunchJobMode) -> bool:
    return mode == LaunchJobMode.ASYNC or mode == LaunchJobMode.ASYNC_FIRE_AND_FORGET


def mode_is_fire_and_forget(mode: LaunchJobMode) -> bool:
    return (
        mode == LaunchJobMode.FIRE_AND_FORGET
        or mode == LaunchJobMode.ASYNC_FIRE_AND_FORGET
    )


# Named this is_wait_for_response instead of is_blocking because the latter
# sounds confusing with async. Maybe we should rename BLOCKING to REGULAR?
def mode_is_wait_for_response(mode: LaunchJobMode) -> bool:
    return mode == LaunchJobMode.ASYNC or mode == LaunchJobMode.BLOCKING


class JetpackException(Exception):
    """Base class for exceptions in this module"""

    pass


class RuntimeException(JetpackException):
    """Exception raised for errors in the Jetpack runtime and kubernetes."""

    def __init__(self, message: str) -> None:
        self.message = message


class ApplicationException(JetpackException):
    """Exception raised for errors from application-code that is using the SDK.

    TODO DEV-157
    For exceptions raised by remote functions and jobs, we serialize the
    userland exception in the backend and save it here. The userland exception
    is re-raised by the SDK for the caller of the remote function or job.
    """

    def __init__(self, message: str) -> None:
        self.message = message


class NoControllerAddressError(JetpackException):
    pass


class Client:
    def __init__(self) -> None:
        host = os.environ.get(
            "JETPACK_RUNTIME_SERVICE_HOST",
            "remotesvc.jetpack-runtime.svc.cluster.local",
        )
        port = os.environ.get("JETPACK_RUNTIME_SERVICE_PORT", "80")
        self.address: str = f"{host.strip()}:{port.strip()}"
        self.stub: Optional[remote_pb2_grpc.RemoteExecutorStub] = None
        self.async_stub: Optional[remote_pb2_grpc.RemoteExecutorStub] = None
        self.dry_run = False
        self.dry_run_last_request: Optional[
            Union[
                remote_pb2.CreateTaskRequest,
                remote_pb2.LaunchBlockingJobRequest,
                remote_pb2.PostResultRequest,
            ]
        ] = None

    def dial(self, mode: LaunchJobMode) -> None:
        if not self.address:
            raise NoControllerAddressError("Controller address is not set")
        # Since this is inter-cluster communication, insecure is fine.
        # In the future this won't even leave the pod, and use a sidecar so
        # it will be localhost.

        # TODO(Landau): When/how should we close the channels?
        if mode_is_async(mode):
            # Warning, this calls asyncio.get_event_loop() which will throw
            # exception if event loop has already been set and closed.
            async_channel = grpc.aio.insecure_channel(self.address)
            self.async_stub = remote_pb2_grpc.RemoteExecutorStub(async_channel)
        else:
            channel = grpc.insecure_channel(self.address)
            self.stub = remote_pb2_grpc.RemoteExecutorStub(channel)

    def launch_job(
        self,
        job: Job[Any],
        args: Optional[Tuple[Any, ...]] = None,
        kwargs: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Launches a k8s job and blocks until the job completes, before returning.
        For now this function assumes job will live in same namespace where the
        launcher is located.

        Keyword arguments:
        job -- job to launch
        module -- jetpack module where the job resides. Used to determine correct
        docker image.
        """
        response = cast(
            remote_pb2.LaunchBlockingJobResponse,
            self._launch_job(LaunchJobMode.BLOCKING, job, uuid.uuid4(), args, kwargs),
        )

        return self._transform_response_exception(response)

    async def launch_async_job(
        self,
        job: Job[Any],
        args: Optional[Tuple[Any, ...]] = None,
        kwargs: Optional[Dict[str, Any]] = None,
    ) -> Any:
        response = cast(
            Awaitable[remote_pb2.LaunchBlockingJobResponse],
            self._launch_job(LaunchJobMode.ASYNC, job, uuid.uuid4(), args, kwargs),
        )

        return self._transform_response_exception(await response)

    def launch_fire_and_forget_job(
        self,
        job: Job[Any],
        args: Optional[Tuple[Any, ...]] = None,
        kwargs: Optional[Dict[str, Any]] = None,
    ) -> Future[Any]:
        """Launches a k8s job. For now this function assumes job will live in
        same namespace where the launcher is located.

        Keyword arguments:
        job -- job to launch
        module -- jetpack module where the job resides. Used to determine correct
        docker image.
        """
        task_id = uuid.uuid4()
        self._launch_job(LaunchJobMode.FIRE_AND_FORGET, job, task_id, args, kwargs)
        return Future(self, task_id)

    async def launch_fire_and_forget_async_job(
        self,
        job: Job[Any],
        args: Optional[Tuple[Any, ...]] = None,
        kwargs: Optional[Dict[str, Any]] = None,
    ) -> Future[Any]:
        task_id = uuid.uuid4()
        await cast(
            Awaitable[remote_pb2.CreateTaskResponse],
            self._launch_job(
                LaunchJobMode.ASYNC_FIRE_AND_FORGET,
                job,
                task_id,
                args,
                kwargs,
            ),
        )
        return Future(self, task_id)

    def post_result(
        self, exec_id: str, value: Any = None, error: Optional[Exception] = None
    ) -> remote_pb2.PostResultResponse:

        if not exec_id:
            # Note: value=None and error=None is acceptable because a job
            # can run successfully and return nothing.
            raise Exception("An exec_id is required to post a result")

        result = remote_pb2.Result()
        if error:
            result.error.code = remote_pb2.APPLICATION
            result.error.message = str(error)
            result.error.encoded_error = bytes(jsonpickle.encode(error), "utf-8")
        else:  # order matters, as 'value' can be None
            result.value.encoded_value = bytes(jsonpickle.encode(value), "utf-8")

        request = remote_pb2.PostResultRequest(
            exec_id=exec_id,
            result=result,
        )

        if self.dry_run:
            self.dry_run_last_request = request
            print(f"Dry Run:\n{request}")
            return remote_pb2.PostResultResponse()

        self._maybe_dial(LaunchJobMode.BLOCKING)
        assert self.stub is not None

        return cast(remote_pb2.PostResultResponse, self.stub.PostResult(request))

    def wait_for_result(self, task_id: uuid.UUID) -> Any:
        request = remote_pb2.WaitForResultRequest(task_id=str(task_id))
        self._maybe_dial(LaunchJobMode.BLOCKING)
        assert self.stub is not None
        return self._transform_response_exception(self.stub.WaitForResult(request))

    def _build_request(
        self,
        mode: LaunchJobMode,
        job: Job[Any],
        task_id: uuid.UUID,
        args: Optional[Tuple[Any, ...]],
        kwargs: Optional[Dict[str, Any]],
    ) -> Union[remote_pb2.CreateTaskRequest, remote_pb2.LaunchBlockingJobRequest]:
        encoded_args = b""
        if args or kwargs:
            encoded_args = codec.encode_args(
                args if args else None,
                kwargs if kwargs else None,
            ).encode("utf-8")

        current_namespace = namespace.get()
        remote_job = remote_pb2.RemoteJob(
            qualified_symbol=job.name(),
            encoded_args=encoded_args,
            hostname=os.environ["HOSTNAME"],  # k8s sets this
            task_id=str(task_id),
            target_time=Timestamp(seconds=int(job.target_time)),
        )
        if current_namespace:
            remote_job.namespace = current_namespace

        request: Union[
            remote_pb2.CreateTaskRequest, remote_pb2.LaunchBlockingJobRequest
        ]

        if mode_is_fire_and_forget(mode):
            request = remote_pb2.CreateTaskRequest(
                job=remote_job, sdk_version=__version__
            )
        elif mode_is_wait_for_response(mode):
            request = remote_pb2.LaunchBlockingJobRequest(
                job=remote_job, sdk_version=__version__
            )

        else:
            raise Exception(f"unsupported mode: {mode}")

        if self.dry_run:
            self.dry_run_last_request = request

        return request

    def _launch_job(
        self,
        mode: LaunchJobMode,
        job: Job[Any],
        task_id: uuid.UUID,
        args: Optional[Tuple[Any, ...]],
        kwargs: Optional[Dict[str, Any]],
    ) -> Union[
        # TODO: Length of this return type makes me thing we should separate
        # the different cases into different implementations.
        remote_pb2.CreateTaskResponse,
        Awaitable[remote_pb2.CreateTaskResponse],
        remote_pb2.LaunchBlockingJobResponse,
        Awaitable[remote_pb2.LaunchBlockingJobResponse],
        None,  # Needed for dry run
        Awaitable[None],  # Needed for dry run
    ]:
        request = self._build_request(mode, job, task_id, args, kwargs)

        # TODO(Landau): This is gross, remove dry_run.
        if self.dry_run:
            if mode_is_async(mode):

                async def empty_awaitable() -> None:
                    pass

                return empty_awaitable()
            return None

        self._maybe_dial(mode)

        if mode == LaunchJobMode.FIRE_AND_FORGET:
            assert self.stub is not None
            return cast(remote_pb2.CreateTaskResponse, self.stub.CreateTask(request))
        elif mode == LaunchJobMode.BLOCKING:
            assert self.stub is not None
            return cast(
                remote_pb2.LaunchBlockingJobResponse,
                self.stub.LaunchBlockingJob(request),
            )

        # Async flavors return a coroutine.
        elif mode == LaunchJobMode.ASYNC:
            assert self.async_stub is not None
            return cast(
                Awaitable[remote_pb2.LaunchBlockingJobResponse],
                self.async_stub.LaunchBlockingJob(request),
            )
        elif mode == LaunchJobMode.ASYNC_FIRE_AND_FORGET:
            assert self.async_stub is not None
            return cast(
                Awaitable[remote_pb2.CreateTaskResponse],
                self.async_stub.CreateTask(request),
            )
        else:
            raise Exception(f"unsupported mode: {mode}")

    @staticmethod
    def _transform_response_exception(
        response: Union[
            remote_pb2.LaunchBlockingJobResponse, remote_pb2.WaitForResultResponse
        ],
    ) -> Any:
        if not isinstance(
            response, remote_pb2.LaunchBlockingJobResponse
        ) and not isinstance(response, remote_pb2.WaitForResultResponse):
            # can happen for dry-run
            # TODO this is a code-smell. We should instead properly mock
            # the response from the grpc call.
            return

        if response.result.HasField("error") and response.result.error.encoded_error:
            e = jsonpickle.decode(response.result.error.encoded_error)
            raise e
        elif response.result.HasField("value"):
            val = jsonpickle.decode(response.result.value.encoded_value)
            return val
        else:
            raise RuntimeException(
                f"Either 'value' or 'error' should be specified in response. Got: {response}"
            )

    def _maybe_dial(self, mode: LaunchJobMode) -> None:
        if not mode_is_async(mode) and self.stub is None:
            self.dial(mode)
        elif mode_is_async(mode) and self.async_stub is None:
            self.dial(mode)
