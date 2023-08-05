from typing import Any, Callable

from jetpack._job.job import Job as _Job
from jetpack.config import symbols


class JobDecorator:
    def __call__(self, fn: Callable[..., Any]) -> Callable[..., Any]:
        job = _Job(fn)
        symbols.get_symbol_table().register(fn)
        return job


# @job will most likely be deprecated in favor of @function.
job = JobDecorator()

# @function is our general remote work decorator. It does not specify how the
# work will be done (RPC, job, queue, etc) and instead leaves that as an
# implementation detail.
# For now, we alias @job, but once/if we remove @job we can refactor other
# internal code
function = JobDecorator()
