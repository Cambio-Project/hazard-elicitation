import json
import re
from typing import Tuple, List

from architecture_extraction_backend.graph.graph import Graph, Node, Edge
from architecture_extraction_backend.arch_models.model import IModel, UnknownOperation


class CyclicServiceOperations(BaseException):
    def __init__(self, nodes: List[Node]):
        super().__init__('Cyclic operations: {}'.format(' -> '.join(map(str, nodes))))


class Architecture:
    """
    Creates a architectural representation of a generic model from services, operations, and dependencies.
    """

    def __init__(self, model: IModel):
        self._model = model
        self._graph = Graph()
        self._hazards = []

        self._build_graph()

    def _build_graph(self):
        temp = None

        # Add nodes
        for _, s in self._model.services.items():
            self._graph.add_node(Node(s.name))

        # Add edges
        for _, s in self._model.services.items():
            for _, o in s.operations.items():
                source = self._graph.node(s.id)

                # Self edge
                if not o.dependencies:
                    self._graph.add_edge(Edge(source, source, o.name))

                else:
                    for d in o.dependencies:
                        target = self._graph.node(d.service.id)

                        # Self edge (already handled)
                        if temp == target:
                            continue

                        temp = target
                        try:
                            self._graph.add_edge(Edge(source, target, o.name))
                        except UnknownOperation(d.service.name, d.name):
                            pass

    @property
    def model(self) -> IModel:
        return self._model

    @property
    def graph(self) -> Graph:
        return self._graph

    def validate(self, check_everything: bool = False) -> Tuple[bool, List[BaseException]]:
        valid = True
        stack = []

        cycle = Graph.check_cycles(self._graph, False)
        if cycle:
            stack.append(CyclicServiceOperations(cycle[0]))

        return valid, stack

    def export(self, pretty: bool = False) -> str:
        result = {'nodes': {}, 'edges': {}, 'hazards': {}}

        for _, n in self._graph.nodes.items():
            result['nodes'][n.id] = {
                'id':    n.id,
                'label': n.label,
                'data':  {
                    'tags': self._model.services[n.label].tags
                }
            }

        for _, e in self._graph.edges.items():
            operation = self._model.services[e.source.label].operations[e.label]
            result['edges'][e.id] = {
                'id':     e.id,
                'label':  e.label,
                'source': e.source.id,
                'target': e.target.id,
                'data':   {
                    'duration': operation.durations,
                    'logs':     operation.logs,
                    'tags':     operation.tags
                }
            }

        for hazard in self._hazards:
            result['hazards'][hazard.id] = {
                'id': hazard.id,
                'type': ''
            }

        if pretty:
            return json.dumps(result, indent=2)
        return json.dumps(result)

    @staticmethod
    def normalize_operation_name(name: str):
        return re.sub(r'^.*(get|put|post)\s*', '', name, flags=re.IGNORECASE) or 'GET /'
