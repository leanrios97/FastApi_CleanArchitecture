from domain.entities.todo import Todo
from domain.repositories.todo_repository import TodoRepository

class UpdateTodoUseCase: 
    def __init__(self, repository: TodoRepository):
        self.repository = repository

    async def execute(self, todo: Todo) -> Todo: 
        return await self.repository.update_todo(todo)
    