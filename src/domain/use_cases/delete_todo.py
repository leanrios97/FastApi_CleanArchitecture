from domain.repositories.todo_repository import TodoRepository

class DeleteTodoUseCase: 
    def __init__(self, repository: TodoRepository):
        self.repository = repository

    async def execute(self, todo_id: int) -> None: 
        return await self.repository.delete_todo(todo_id)
        