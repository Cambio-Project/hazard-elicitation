import json

from architecture_extraction_backend.arch_models.model import IModel
from typing import Union, Any, Dict, List

from typing.io import IO

from architecture_extraction_backend.arch_models.operation import Operation
from architecture_extraction_backend.arch_models.service import Service


class ZipkinTrace(IModel):
    def __init__(self, source: Union[str, IO, list] = None, multiple: bool = False):
        super().__init__(self.__class__.__name__, source, multiple)

    def _parse_multiple(self, model: List[List[Dict[str, Any]]]) -> bool:
        multiple = [trace for trace_list in model for trace in trace_list]
        return self._parse(multiple)

    def _parse(self, model: List[Dict[str, Any]]) -> bool:
        # Store span_id: span
        span_ids = {}

        # Store all services
        for span in model:
            span_ids[span['id']] = span
            local = span.get('localEndpoint', {})
            remote = span.get('remoteEndpoint', {})

            local_endpoint = local.get('serviceName', '')
            remote_endpoint = remote.get('serviceName', '')

            if local_endpoint not in self._services:
                service = Service(local_endpoint)
                service.tags = local
                self._services[local_endpoint] = service

            if remote_endpoint not in self._services:
                service = Service(remote_endpoint)
                service.tags = remote
                self._services[remote_endpoint] = service

        # Add operations
        for span in model:
            local = span.get('localEndpoint', {})
            service_name = local.get('serviceName', '')

            # Unknown service
            if not service_name:
                return False

            operation_name = span['name']
            if operation_name in self.services[service_name].operations:
                operation = self.services[service_name].operations[operation_name]
            else:
                operation = Operation(operation_name)
                self._services[service_name].add_operation(operation)

            span_id = span['id']
            operation.durations[span_id] = span.get('duration', -1)
            operation.tags[span_id] = span.get('tags', {})
            operation.logs[span_id] = {a['timestamp']: {'log': a['value']} for a in span.get('annotations', {})}

        # Add dependencies
        for span in model:
            if span.get('parentId', 0) in span_ids:

                # Callee
                local = span.get('localEndpoint', {})
                service_name = local.get('serviceName', '')
                operation_name = span['name']

                operation = self._services[service_name].operations[operation_name]

                # Caller
                parent_id = span['parentId']
                parent_span = span_ids[parent_id]
                parent = parent_span.get('localEndpoint', {})
                parent_service_name = parent.get('serviceName', '')
                parent_operation_name = parent_span['name']

                parent_operation = self._services[parent_service_name].operations[parent_operation_name]
                skip = False
                for dependency in parent_operation.dependencies:
                    if dependency.name == operation_name:
                        skip = True
                        break

                if not skip:
                    parent_operation.add_dependency(operation)

        return True

    def read_multiple(self, source: Union[str, IO, list] = None) -> bool:
        if isinstance(source, str):
            return self._parse_multiple(json.load(open(source, 'r')))
        elif isinstance(source, IO):
            return self._parse_multiple(json.load(source))
        elif isinstance(source, list):
            return self._parse_multiple(source)
        return False

    def read(self, source: Union[str, IO, list] = None) -> bool:
        if isinstance(source, str):
            return self._parse(json.load(open(source, 'r')))
        elif isinstance(source, IO):
            return self._parse(json.load(source))
        elif isinstance(source, list):
            return self._parse(source)
        return False
