from typing import List
from domain.entities.todo import Todo
from domain.repositories.todo_repository import TodoRepository
from config import logger

class ListTodosUseCase: 
    def __init__(self, repository: TodoRepository):
        self.repository = repository

    async def execute(self) -> List[Todo]: 
        result = await self.repository.list_all()
        logger.info(f"ListTodosUseCase executed: List task id={result.id}, title={result.title}")

        return result