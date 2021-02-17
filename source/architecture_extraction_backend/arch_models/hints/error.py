from architecture_extraction_backend.arch_models.hints.hint import Hint


class Error(Hint):
    def __init__(self):
        super().__init__()


class UnknownOperation(Hint):
    def __init__(self, operation):
        super().__init__()
        self._operation = operation

    def __str__(self):
        return self._operation
