from typing import Tuple, List

from architecture_extraction_backend.arch_models.architecture import Architecture
from architecture_extraction_backend.arch_models.model import IModel


class Validator:
    @staticmethod
    def validate_model(model: IModel) -> Tuple[bool, List[BaseException]]:
        return model.validate(True)

    @staticmethod
    def validate_architecture(arch: Architecture) -> Tuple[bool, List[BaseException]]:
        return arch.validate()
