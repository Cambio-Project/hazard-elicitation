import json

from archex_backend.models.model import IModel
from typing import Union, Any, Dict

from typing.io import IO

from archex_backend.models.operation import Operation
from archex_backend.models.service import Service


class JaegerTrace(IModel):
    def __init__(self, source: Union[str, IO] = None):
        super().__init__(self.__class__.__name__, source)

    def _parse(self, model: Dict[str, Any]) -> bool:
        # Store process_id: service_name
        process_ids = {}
        # Store span_id: span
        span_ids = {}
        traces = model['data']

        for trace in traces:
            # Identify all services (processes)
            for process_id, process in trace['processes'].items():
                service_name = process['serviceName']
                self._services[service_name] = Service(service_name)
                process_ids[process_id] = service_name

            # Add operations to the corresponding services.
            for span in trace['spans']:
                span_ids[span['spanID']] = span
                operation_name = span['operationName']
                pid = span['processID']

                # Unknown process
                if pid not in process_ids:
                    return False

                service_name = process_ids[pid]
                operation = Operation(operation_name)
                self._services[service_name].add_operation(operation)

            # Add dependencies
            for span in trace['spans']:
                for reference in span['references']:
                    if reference['refType'] == 'CHILD_OF':

                        # Callee
                        pid = span['processID']
                        service_name = process_ids[pid]
                        operation_name = span['operationName']

                        operation = self._services[service_name].operations[operation_name]

                        # Caller
                        parent_id = reference['spanID']
                        parent_span = span_ids[parent_id]
                        parent_pid = parent_span['processID']
                        parent_service_name = process_ids[parent_pid]
                        parent_operation_name = parent_span['operationName']

                        parent_operation = self._services[parent_service_name].operations[parent_operation_name]
                        parent_operation.add_dependency(operation)

        return True

    def read(self, source: Union[str, IO] = None) -> bool:
        if isinstance(source, str):
            return self._parse(json.load(open(source, 'r')))
        elif isinstance(source, IO):
            return self._parse(json.load(source))
        return False
