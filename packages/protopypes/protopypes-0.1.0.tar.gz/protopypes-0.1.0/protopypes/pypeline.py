"""module for ETL-Pipeline class.

The pipeline currently has the following properties and functions:
    - register_task: registers a task inside the pipeline
    - len: length of tasks currently registered
    - run(): runs the pipeline


"""

# base imports
import logging

# type hints imports
from typing import Callable, Dict, List
from .step import PypelineStep, ExecutionError
from .models import PypelineStepFunction

# dependencies
from collections import deque


class Pypeline:
    """main pipeline class for etl processes."""

    logger = logging.getLogger(__name__)

    def __init__(self, *args: List[PypelineStep], **kwargs):
        self.__registered_steps = deque(args)
        self.__pypeline_vars: Dict = kwargs

    def register_step(self, func: PypelineStepFunction) -> PypelineStepFunction:
        self.__registered_steps.append(PypelineStep(func))

    # Decorators
    # todo Add options
    def step(self) -> Callable[[PypelineStepFunction], PypelineStepFunction]:
        """register task at queue"""

        def register_step(func: PypelineStepFunction) -> PypelineStepFunction:
            self.__registered_steps.append(PypelineStep(func))
            return func

        return register_step

    # main functionality
    # ToDo clarify if its possible to use __call__
    def run(self):
        try:
            for step in self.__registered_steps:
                self.logger.debug(f"Running step {step.__name__}")
                step.execute()

        except ExecutionError as e:
            self.logger.error(f"Encountered Error during pipeline execution. {e}")
            # To Do: Enable On_Error Option for Step
            raise e

    # base class functions and properties
    @property
    def steps(self) -> Dict:
        return {step.__name__: step.__doc__ for step in self.__registered_steps}

    @property
    def variables(self) -> List[str]:
        return self.__pypeline_vars

    @variables.setter
    def variables(self, new_args) -> None:
        self.__pypeline_vars.update(new_args)

    @variables.deleter
    def variables(self) -> None:
        self.__pypeline_vars = dict()

    @property
    def len(self):
        return len(self.__registered_steps)

    def __len__(self):
        return len(self.__registered_steps)

    def __eq__(self, other):
        if not isinstance(other, self.__class__) or self.len != other.len:
            return False
        else:
            return all([self.steps[i] == other.steps[i] for i in range(len(self))])
