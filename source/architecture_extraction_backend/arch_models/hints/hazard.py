class Keyword:
    NO = 'no'
    NOT = 'not'
    LESS = 'less than'
    MORE = 'more than'
    OTHER = 'other than'


class Metric:
    AVAILABILITY = 'availability'
    RESPONSE_TIME = 'response time'
    THROUGHPUT = 'throughput'


class Consequence:
    MINOR = 1, 'minor'
    SERIOUS = 2, 'serious'
    CRITICAL = 3, 'critical'


class Likelihood:
    UNLIKELY = 1, 'unlikely'
    POSSIBLE = 2, 'possible'
    PROBABLE = 3, 'probable'


class Hazard:
    ID = 0

    def __init__(self):
        self._id = Hazard.get_id()
        self._keyword = Keyword.NO
        self._metric = Metric.AVAILABILITY
        self._type = 'Architecture'
        self._consequence = Consequence.MINOR
        self._likelihood = Likelihood.UNLIKELY
        self._severity = self._consequence[0] * self._likelihood[0]

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.id)

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def get_id():
        Hazard.ID += 1
        return Hazard.ID

    @property
    def id(self):
        return self._id

    @property
    def keyword(self):
        return self._keyword

    @property
    def metric(self):
        return self._metric

    @property
    def type(self):
        return self._type

    @property
    def consequence(self):
        return self._consequence

    @property
    def likelihood(self):
        return self._likelihood

    @property
    def severity(self):
        return self._severity


class OperationHazard(Hazard):
    def __init__(self):
        super().__init__()


class WorkloadDeviation(OperationHazard):
    def __init__(self):
        super().__init__()


class PeekWorkload(OperationHazard):
    def __init__(self):
        super().__init__()
