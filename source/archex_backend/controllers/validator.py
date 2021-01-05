from typing import Tuple, List

from archex_backend.models.architecture import Architecture
from archex_backend.models.model import IModel


class Validator:
    @staticmethod
    def validate_model(model: IModel) -> Tuple[bool, List[BaseException]]:
        return model.validate(True)

    @staticmethod
    def validate_architecture(arch: Architecture) -> Tuple[bool, List[BaseException]]:
        return arch.validate()
