import json

from architecture_extraction_backend.arch_models.model import IModel
from typing import Union, Any, Dict

from typing.io import IO

from architecture_extraction_backend.arch_models.operation import Operation
from architecture_extraction_backend.arch_models.service import Service


class JaegerTrace(IModel):
    def __init__(self, source: Union[str, IO, dict] = None):
        super().__init__(self.__class__.__name__, source)

    @staticmethod
    def _parse_logs(logs) -> Dict[int, Dict[str, str]]:
        operation_logs = {}
        for log in logs:
            operation_logs[log['timestamp']] = {f['key']: f['value'] for f in log['fields']}

        return operation_logs

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

                service = Service(service_name)
                service.tags = {tag['key']: tag['value'] for tag in process['tags']}
                service.tags['serviceName'] = service_name

                self._services[service_name] = service
                process_ids[process_id] = service_name

            # Add operations to the corresponding services.
            for span in trace['spans']:
                pid = span['processID']

                # Unknown process
                if pid not in process_ids:
                    return False

                span_ids[span['spanID']] = span
                operation_name = span['operationName']
                operation_duration = span['duration']
                operation_tags = span['tags']
                operation_logs = span['logs']

                operation = Operation(operation_name)
                operation.duration = operation_duration
                operation.tags = {tag['key']: tag['value'] for tag in operation_tags}
                operation.logs = JaegerTrace._parse_logs(operation_logs)

                service_name = process_ids[pid]
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

    def read(self, source: Union[str, IO, dict] = None) -> bool:
        if isinstance(source, str):
            return self._parse(json.load(open(source, 'r')))
        elif isinstance(source, IO):
            return self._parse(json.load(source))
        elif isinstance(source, dict):
            return self._parse(source)
        return False
