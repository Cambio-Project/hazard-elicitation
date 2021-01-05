class Node:
    def __init__(self, name: str = ''):
        self._label = name
        self._id = -1

    def __repr__(self) -> str:
        return '{} {} ({})'.format(self.__class__.__name__, self._id, self._label)

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, node_id: int):
        self._id = node_id

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, label: str):
        self._label = label
