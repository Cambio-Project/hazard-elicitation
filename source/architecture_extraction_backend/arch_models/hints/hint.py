class Category:
    ARCHITECTURE = 'Architecture'
    METRIC = 'Metric'


class Hint:
    def __init__(self):
        self._category = ''
        self._type = ''
        self._severity = ''
        self._impact = ''

    def __repr__(self):
        return '{}({}|{})'.format(self.__class__.__name__, self._category, self._type)

    def __str__(self):
        return self.__repr__()
