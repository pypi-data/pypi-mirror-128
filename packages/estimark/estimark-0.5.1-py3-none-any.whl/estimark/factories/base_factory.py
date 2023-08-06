from injectark import Factory
from ..core.common import Config
from ..application.domain.common import QueryParser
from ..application.domain.repositories import (
    TaskRepository, MemoryTaskRepository,
    LinkRepository, MemoryLinkRepository,
    ClassifierRepository, MemoryClassifierRepository,
    ClassificationRepository, MemoryClassificationRepository,
    ScheduleRepository, MemoryScheduleRepository,
    SlotRepository, MemorySlotRepository)
from ..application.domain.services import PlotService, MemoryPlotService
from ..application.managers import EstimationManager, InitializationManager
from ..application.informers import EstimarkInformer, StandardEstimarkInformer


class BaseFactory(Factory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.config = config

    def query_parser(self) -> QueryParser:
        return QueryParser()

    def task_repository(
            self, query_parser: QueryParser
    ) -> TaskRepository:
        return MemoryTaskRepository(query_parser)

    def link_repository(
            self, query_parser: QueryParser
    ) -> LinkRepository:
        return MemoryLinkRepository(query_parser)

    def classifier_repository(
            self, query_parser: QueryParser
    ) -> ClassifierRepository:
        return MemoryClassifierRepository(query_parser)

    def classification_repository(
            self, query_parser: QueryParser
    ) -> ClassificationRepository:
        return MemoryClassificationRepository(query_parser)

    def schedule_repository(
            self, query_parser: QueryParser
    ) -> ScheduleRepository:
        return MemoryScheduleRepository(query_parser)

    def slot_repository(
            self, query_parser: QueryParser
    ) -> SlotRepository:
        return MemorySlotRepository(query_parser)

    def plot_service(self) -> PlotService:
        return MemoryPlotService()

    def estimation_manager(
            self, task_repository: TaskRepository,
            classifier_repository: ClassifierRepository,
            classification_repository: ClassificationRepository,
            link_repository: LinkRepository,
            schedule_repository: ScheduleRepository,
            slot_repository: SlotRepository,
            plot_service: PlotService
    ) -> EstimationManager:
        return EstimationManager(
            task_repository, classifier_repository,
            classification_repository, link_repository,
            schedule_repository, slot_repository, plot_service)

    def initialization_manager(
            self, classifier_repository: ClassifierRepository,
    ) -> InitializationManager:
        return InitializationManager(classifier_repository)

    def estimark_informer(
            self, task_repository: TaskRepository,
            link_repository: LinkRepository,
            classifier_repository: ClassifierRepository,
            schedule_repository: ScheduleRepository,
            slot_repository: SlotRepository
    ) -> EstimarkInformer:
        return StandardEstimarkInformer(
            task_repository, link_repository, classifier_repository,
            schedule_repository, slot_repository)
