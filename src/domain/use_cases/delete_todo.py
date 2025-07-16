from domain.repositories.todo_repository import TodoRepository
from config import logger

class DeleteTodoUseCase: 
    def __init__(self, repository: TodoRepository):
        self.repository = repository

    async def execute(self, todo_id: int) -> None: 

        result = await self.repository.delete_todo(todo_id) 
        logger.info(f"DeleteTodoUseCase executed: delete task id={result.id}, title={result.title}")

        return result
        