"""module to define class that describes etl step in pipeline"""
from .base import BaseStep
from .models import PypelineStepFunction


class ExecutionError(Exception):
    pass


class PypelineStep(BaseStep):
    def __init__(self, f: PypelineStepFunction, **kwargs) -> None:
        self.__callable = f
        self.__name__ = f.__name__
        self.__doc__ = f.__doc__
        self._params = kwargs

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, new_params: dict):
        self._params = new_params

    def execute(self):
        try:
            erg = self.__callable(**self._params)
            return erg
        except Exception as e:
            raise ExecutionError(
                f"Failed to execute step {self.__name__} due to error: {e}"
            )
