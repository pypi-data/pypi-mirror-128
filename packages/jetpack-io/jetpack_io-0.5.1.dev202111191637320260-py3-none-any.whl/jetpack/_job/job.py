from __future__ import annotations

import asyncio
import base64
import inspect
import time
from typing import Any, Awaitable, Callable, Dict, Generic, Tuple, TypeVar, Union, cast

from jetpack import utils
from jetpack._job.client import Client
from jetpack._job.future import Future
from jetpack._remote import codec

T = TypeVar("T")

client = Client()


def get_client() -> Client:
    return client


class AlreadyExistsError(Exception):
    pass


class Job(Generic[T]):
    # Question: do we need a separate Dict for blocking jobs?
    jobs: Dict[str, Job[Any]] = {}

    def __init__(self, func: Callable[..., Union[T, Awaitable[T]]]) -> None:
        self.func = func
        self.target_time = int(time.time())

    def __call__(self, *args: Any, **kwargs: Any) -> Union[Any, Awaitable[Any]]:
        """
        No return value for now, but eventually this will return a handle
        or an awaitable
        """
        if inspect.iscoroutinefunction(self.func):
            return client.launch_async_job(self, args, kwargs)
        else:
            return client.launch_job(self, args, kwargs)

    def launch(
        self, *args: Any, **kwargs: Any
    ) -> Union[Future[T], Awaitable[Future[T]]]:
        if inspect.iscoroutinefunction(self.func):
            return cast(
                Awaitable[Future[T]],
                client.launch_fire_and_forget_async_job(self, args, kwargs),
            )
        else:
            return cast(
                Future[T],
                client.launch_fire_and_forget_job(self, args, kwargs),
            )

    def schedule(self, target_time: int) -> Job[T]:
        self.target_time = target_time
        return self

    def name(self) -> str:
        return utils.qualified_func_name(self.func)

    def exec(self, exec_id: str, base64_encoded_args: str = "") -> None:

        args: Tuple[Any, ...] = ()
        kwargs: Dict[str, Any] = {}
        if base64_encoded_args:
            encoded_args = base64.b64decode(base64_encoded_args).decode("utf-8")
            decoded_args, decoded_kwargs = codec.decode_args(encoded_args)
            if decoded_args:
                args = decoded_args
            if decoded_kwargs:
                kwargs = decoded_kwargs

        retval, err = None, None
        try:
            if inspect.iscoroutinefunction(self.func):
                func = cast(Awaitable[T], self.func(*args, **kwargs))
                retval = asyncio.run(func)
            else:
                retval = cast(T, self.func(*args, **kwargs))
        except Exception as e:
            err = e

        # for now, we post the result back to the remotesvc. A slightly better approach is to
        # have the caller of this function post it (the CLI). Doing it here for now because
        # the remotesvc is already initialized and set up here.
        client.post_result(exec_id, value=retval, error=err)
