from typing import List

from architecture_extraction_backend.arch_models.hazard import Hazard
from architecture_extraction_backend.arch_models.model import IModel


class Analyzer:
    @staticmethod
    def analyze_model(model: IModel) -> List[Hazard]:
        return model.analyze()
