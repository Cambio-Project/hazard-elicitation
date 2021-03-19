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
        # Store ip: service_name
        service_ips = {}
        # Store span_id: span
        span_ids = {}

        # Store all services with their respective endpoint ip's
        for span in model:
            span_ids[span['id']] = span
            local = span['localEndpoint'] if 'localEndpoint' in span else {}
            remote = span['remoteEndpoint'] if 'remoteEndpoint' in span else {}

            source_name = local['serviceName'] if 'serviceName' in local else ''
            target_name = remote['serviceName'] if 'serviceName' in remote else ''

            if source_name:
                if source_name not in self._services:
                    source = Service(source_name)
                    source.tags = local
                    self._services[source_name] = source

                service_ips[local['ipv4']] = source_name

            if target_name:
                if target_name not in self._services:
                    target = Service(target_name)
                    target.tags = remote
                    self._services[target_name] = target

                service_ips[remote['ipv4']] = target_name

        # Add operations
        for span in model:
            local = span['localEndpoint'] if 'localEndpoint' in span else {}
            if local['ipv4'] in service_ips:
                service_name = service_ips[local['ipv4']]
            elif 'serviceName' in local and local['serviceName'] in self._services:
                service_name = local['serviceName']
            # Unknown service
            else:
                return False

            operation_name = span['name']
            operation_duration = span.get('duration', -1)
            operation_tags = span.get('tags', {})
            operation_annotation = span.get('annotations', {})

            if operation_name in self.services[service_name].operations:
                operation = self.services[service_name].operations[operation_name]
            else:
                operation = Operation(operation_name)
                self._services[service_name].add_operation(operation)

            span_id = span['id']
            operation.durations[span_id] = operation_duration
            operation.tags[span_id] = operation_tags
            operation.logs[span_id] = {a['timestamp']: {'log': a['value']} for a in operation_annotation}

        # Add dependencies
        for span in model:
            if 'parentId' in span:

                # Callee
                service_name = span['localEndpoint']['serviceName']
                operation_name = span['name']

                if operation_name not in self._services[service_name].operations:
                    continue

                operation = self._services[service_name].operations[operation_name]

                # Caller
                parent_id = span['parentId']
                if parent_id not in span_ids:
                    continue
                parent_span = span_ids[parent_id]
                local = parent_span['localEndpoint']
                parent_service_name = service_ips[local['ipv4']]
                parent_operation_name = parent_span['name']

                parent_operation = self._services[parent_service_name].operations[parent_operation_name]
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
