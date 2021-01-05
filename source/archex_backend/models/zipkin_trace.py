import json

from archex_backend.models.model import IModel
from typing import Union, Any, Dict, List

from typing.io import IO

from archex_backend.models.operation import Operation
from archex_backend.models.service import Service


class ZipkinTrace(IModel):
    def __init__(self, source: Union[str, IO] = None):
        super().__init__(self.__class__.__name__, source)

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
                    self._services[source_name] = source
                    service_ips[local['ipv4']] = source_name

            if target_name:
                if target_name not in self._services:
                    source = Service(target_name)
                    self._services[target_name] = source
                    service_ips[remote['ipv4']] = target_name

        # Add operations
        for span in model:
            local = span['localEndpoint'] if 'localEndpoint' in span else {}
            if local['ipv4'] in service_ips:
                service = service_ips[local['ipv4']]
            elif 'serviceName' in local and local['serviceName'] in self._services:
                service = local['serviceName']
            # Unknown service
            else:
                return False

            self._services[service].add_operation(Operation(span['name']))

        # Add dependencies
        for span in model:
            if 'parentId' in span:

                # Callee
                service_name = span['localEndpoint']['serviceName']
                operation_name = span['name']
                operation = self._services[service_name].operations[operation_name]

                # Caller
                parent_id = span['parentId']
                parent_span = span_ids[parent_id]
                local = parent_span['localEndpoint']
                parent_service_name = service_ips[local['ipv4']]
                parent_operation_name = parent_span['name']

                parent_operation = self._services[parent_service_name].operations[parent_operation_name]
                parent_operation.add_dependency(operation)

        return True

    def read(self, source: Union[str, IO] = None) -> bool:
        if isinstance(source, str):
            return self._parse(json.load(open(source, 'r')))
        elif isinstance(source, IO):
            return self._parse(json.load(source))
        return False
