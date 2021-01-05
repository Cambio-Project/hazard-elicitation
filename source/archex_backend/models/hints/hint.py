class Category:
    ARCHITECTURE = 'Architecture'
    METRIC = 'Metric'


class Hint:
    def __init__(self):
        self._category = ''
        self._type = ''
        self._severity = ''
        self._stakeholder = ''

    def __str__(self):
        pass

    def __repr__(self):
        pass
