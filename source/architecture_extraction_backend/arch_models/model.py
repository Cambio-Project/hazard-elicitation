from typing import Union, Dict, Tuple, List, Any
from typing.io import IO
import pandas as pd

from architecture_extraction_backend.arch_models.hints.hazard import Hazard, WorkloadDeviation
from architecture_extraction_backend.arch_models.operation import Operation
from architecture_extraction_backend.arch_models.service import Service
from util.log import tb


class NoDependenciesException(BaseException):
    def __init__(self):
        super().__init__('No dependencies found')


class WrongFormatException(BaseException):
    def __init__(self):
        super().__init__('Wrong format')


class UnknownOperation(BaseException):
    def __init__(self, service: str, operation: str):
        super().__init__('Unknown Operation: {}/{}'.format(service, operation))


class OperationSelfDependency(BaseException):
    def __init__(self, operation: Operation):
        if operation.service:
            operation = '{}/{}'.format(operation.service.name, operation.name)
        super().__init__('Self Dependency: {}'.format(operation))


class CyclicOperationDependency(BaseException):
    def __init__(self, operation1: Operation, operation2: Operation):
        if operation1.service:
            operation1 = '{}/{}'.format(operation1.service.name, operation1.name)
        if operation2.service:
            operation2 = '{}/{}'.format(operation2.service.name, operation2.name)
        super().__init__('Circular Dependency: {} <-> {}'.format(operation1, operation2))


class IModel:
    """
    Interface for all models.
    All derived classes must implement the read method.
    The read method is responsible to check the syntax of the model.

    IModel provides a validation method that checks for validity of the model.
    This validation checks the semantic of the model.
    """
    def __init__(self, model_type: str, source: Union[str, IO] = None):
        self._model_type = model_type
        self._services = {}
        self._valid = False
        self._hazards = []

        if source:
            try:
                if not self.read(source):
                    print('Model was not read successful')
            except BaseException as e:
                print(tb(e))
                print('Something went wrong')

    def __iter__(self):
        return iter(self._services)

    @property
    def type(self) -> str:
        return self._model_type

    @property
    def services(self) -> Dict[str, Service]:
        return self._services

    @property
    def valid(self) -> bool:
        return self._valid

    @property
    def hazards(self) -> List[Hazard]:
        return self._hazards

    @hazards.setter
    def hazards(self, hazards: List[Hazard]):
        self._hazards = hazards

    # Private

    def _parse(self, model: Dict[str, Any]) -> bool:
        raise NotImplementedError('_parse() method must be implemented!')

    # Public

    def validate(self, check_everything=False) -> Tuple[bool, List[BaseException]]:
        valid = True
        stack = []

        try:
            for _, service in self._services.items():
                for _, operation in service.operations.items():

                    # Check self dependency
                    if operation in operation.dependencies:
                        stack.append(OperationSelfDependency(operation))

                    for dependency in operation.dependencies:
                        # Check circular dependencies
                        if operation in dependency.dependencies:
                            stack.append(CyclicOperationDependency(operation, dependency))
                            continue

                        try:
                            _ = self._services[dependency.service.label].operations[dependency.label]

                        # Service or operation is not known.
                        except AttributeError:
                            if not check_everything:
                                return False, [UnknownOperation(service.label, operation.label)]
                            else:
                                valid = False
                                stack.append(UnknownOperation(service.label, operation.label))

        # Unknown exception has occurred.
        except BaseException as e:
            stack.append(e)
            return False,  stack

        self._valid = valid
        return valid, stack

    def analyze(self) -> List[Hazard]:
        stack = []

        try:
            for service_name, service in self._services.items():
                for operation_name, operation in service.operations.items():
                    series = pd.Series(operation.durations.values())
                    # Filter outliers by 3 times standard deviation
                    series = series[~((series-series.mean()).abs() > series.std() * 3)]
                    diff = 1 - series.min() / series.max()

                    # Min and Max response times differ by at least 50%
                    if diff > 0.5:
                        stack.append(WorkloadDeviation())

            return stack
        except BaseException as e:
            tb(e)
            return stack

    def print(self):
        for _, service in self._services.items():
            service.print()

    def read(self, source: Union[str, IO]) -> bool:
        raise NotImplementedError('read() method must be implemented!')
