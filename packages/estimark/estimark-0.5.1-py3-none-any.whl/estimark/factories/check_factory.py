from ..core.common import Config
from ..application.domain.models import Task
from ..application.domain.common import QueryParser
from ..application.domain.repositories import (
    TaskRepository, MemoryTaskRepository)
from .base_factory import BaseFactory


class CheckFactory(BaseFactory):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.config = config

    # Repositories
    def task_repository(
            self, query_parser: QueryParser
    ) -> TaskRepository:

        task_repository = super().task_repository(query_parser)

        task_repository.load({'data': {
            "1": Task(id='1', name='Define WBS'),
            "2": Task(id='2', name='Deploy Servers'),
            "3": Task(id='3', name='Design Website')
        }})
        return task_repository
