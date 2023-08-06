from ..core.common import Config
from ..application.domain.common import QueryParser
from ..application.domain.repositories import (
    TaskRepository, LinkRepository, ClassificationRepository)
from ..core.data import (
    RstTaskRepository, RstLinkRepository,
    RstAnalyzer, RstLoader, RstClassificationRepository)
from .json_factory import JsonFactory


class RstFactory(JsonFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.config = config

    def rst_analyzer(self):
        return RstAnalyzer()

    def rst_loader(self, analyzer: RstAnalyzer):
        root = self.config['root_dir']
        return RstLoader(root, analyzer)

    def task_repository(
        self, query_parser: QueryParser, loader: RstLoader
    ) -> TaskRepository:
        repository = RstTaskRepository(query_parser, loader)
        repository.load()
        return repository

    def link_repository(
        self, query_parser: QueryParser, loader: RstLoader
    ) -> RstLinkRepository:
        repository = RstLinkRepository(query_parser, loader)
        repository.load()
        return repository

    def classification_repository(
        self, query_parser: QueryParser, loader: RstLoader
    ) -> ClassificationRepository:
        repository = RstClassificationRepository(query_parser, loader)
        repository.load()
        return repository
