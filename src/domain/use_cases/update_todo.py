from domain.entities.todo import Todo
from domain.repositories.todo_repository import TodoRepository
from config import logger

class UpdateTodoUseCase: 
    def __init__(self, repository: TodoRepository):
        self.repository = repository

    async def execute(self, todo: Todo) -> Todo: 

        result = await self.repository.update_todo(todo)
        logger.info(f"UpdateTodoUseCase executed: update task id={result.id}, title={result.title}")

        return result
    