from typing import Optional
from domain.entities.todo import Todo
from domain.repositories.todo_repository import TodoRepository
from config import logger

class GetTodoUseCase: 
    def __init__(self, repository: TodoRepository):
        self.repository = repository

    async def execute(self, todo_id: int) -> Optional[Todo]: 
        result = await self.repository.get_by_id(todo_id)
        logger.info(f"GetTodoUseCase executed: Get_id task id={result.id}, title={result.title}")

        return result
    
        