import json
from typing import Tuple, List

from archex_backend.graph.graph import Graph, Node, Edge
from archex_backend.models.model import IModel, UnknownOperation


class CyclicServiceOperations(BaseException):
    def __init__(self, nodes: List[Node]):
        super().__init__('Cyclic operations: {}'.format(' -> '.join(map(str, nodes))))


class Architecture:
    """

    """
    def __init__(self, model: IModel):
        self._model = model
        self._graph = Graph()

        self._build_graph()

    def _build_graph(self):
        temp = None

        for _, s in self._model.services.items():
            self._graph.add_node(Node(s.name))

        for _, s in self._model.services.items():
            for _, o in s.operations.items():
                source = self._graph.node(s.name)

                if not o.dependencies:
                    self._graph.add_edge(Edge(source, source, o.name))

                else:
                    for d in o.dependencies:
                        target = self._graph.node(d.service.label)

                        if temp == target:
                            continue

                        temp = target
                        try:
                            self._graph.add_edge(Edge(source, target, o.name))
                        except UnknownOperation(d.service.label, d.label):
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

    def d3_graph(self, pretty: bool = False) -> str:
        result = {'nodes': [], 'links': []}

        for n_id, n in self._graph.nodes.items():
            result['nodes'].append({
                'label': n.label,
                'id': n_id
            })

        for e in self._graph.edges:
            result['links'].append({
                'id': e.id,
                'label': e.label,
                'source': e.source.id,
                'target': e.target.id
            })

        if pretty:
            return json.dumps(result, indent=2)
        return json.dumps(result)
