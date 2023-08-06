from ..core.common import Config
from ..application.domain.common import QueryParser
from ..application.domain.repositories import (
    TaskRepository, LinkRepository, ClassifierRepository,
    ClassificationRepository, ScheduleRepository, SlotRepository)
from ..core.data.json import (
    init_json_database, JsonRepository,
    JsonClassificationRepository, JsonClassifierRepository,
    JsonLinkRepository, JsonScheduleRepository,
    JsonSlotRepository, JsonTaskRepository)
from .altair_factory import AltairFactory


class JsonFactory(AltairFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.config = config
        self.param_dir = self.config['param_dir']
        self.result_dir = self.config['result_dir']

    def classification_repository(
        self, query_parser: QueryParser,
    ) -> ClassificationRepository:
        return JsonClassificationRepository(
            self.param_dir, query_parser, file_suffix='param')

    def classifier_repository(
        self, query_parser: QueryParser,
    ) -> ClassifierRepository:
        return JsonClassifierRepository(
            self.param_dir, query_parser, file_suffix='param')

    def link_repository(
        self, query_parser: QueryParser,
    ) -> LinkRepository:
        return JsonLinkRepository(
            self.param_dir, query_parser, file_suffix='param')

    def schedule_repository(
        self, query_parser: QueryParser,
    ) -> ScheduleRepository:
        return JsonScheduleRepository(
            self.result_dir, query_parser, file_suffix='result')

    def slot_repository(
        self, query_parser: QueryParser,
    ) -> SlotRepository:
        return JsonSlotRepository(
            self.result_dir, query_parser, file_suffix='result')

    def task_repository(
        self, query_parser: QueryParser,
    ) -> TaskRepository:
        return JsonTaskRepository(
            self.param_dir, query_parser, file_suffix='param')
