from typing import TypeVar, Callable, Any

PypelineStepFunction = TypeVar("PypelineStepFunction", bound=Callable[..., Any])
