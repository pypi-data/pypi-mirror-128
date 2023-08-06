from typing import List, Dict, Any
from ..domain.common import QueryDomain
from ..domain.models import Classifier
from ..domain.repositories import ClassifierRepository
from ..domain.services import PlotService


class InitializationManager:
    def __init__(self, classifier_repository: ClassifierRepository) -> None:
        self.classifier_repository = classifier_repository

    def initialize(self) -> None:
        classifiers = self.classifier_repository.search([])
        if classifiers:
            return

        self.classifier_repository.add([
            Classifier(id='XS', name='Extra Small', amount=1),
            Classifier(id='S', name='Small', amount=2),
            Classifier(id='M', name='Medium', amount=3),
            Classifier(id='L', name='Large', amount=5),
            Classifier(id='XL', name='Extra Large', amount=8),
            Classifier(id='DAY', name='Day', amount=1),
            Classifier(id='WEEK', name='Week', amount=7),
            Classifier(id='MONTH', name='Month', amount=30),
            Classifier(id='SEM', name='SEM', amount=180)
        ])
