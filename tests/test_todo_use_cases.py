import pytest
from src.domain.entities.todo import Todo
from src.domain.use_cases.create_todo import CreateTodoUseCase
from src.domain.use_cases.get_todo import GetTodoUseCase
from src.domain.use_cases.list_todos import ListTodosUseCase
from src.domain.use_cases.update_todo import UpdateTodoUseCase
from src.domain.use_cases.delete_todo import DeleteTodoUseCase
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_create_todo_use_case():
    repository = AsyncMock()
    use_case = CreateTodoUseCase(repository)
    todo = await use_case.execute("Test", "Description")
    assert todo.title == "Test"
    assert todo.description == "Description"
    assert todo.completed is False

@pytest.mark.asyncio
async def test_get_todo_use_case():
    repository = AsyncMock()
    repository.get_by_id.return_value = Todo(id=1, title="Test", description="Description", completed=False, created_at=None)
    use_case = GetTodoUseCase(repository)
    todo = await use_case.execute(1)
    assert todo.id == 1
    assert todo.title == "Test"

@pytest.mark.asyncio
async def test_list_todos_use_case():
    repository = AsyncMock()
    repository.list_all.return_value = [Todo(id=1, title="Test", description="Description", completed=False, created_at=None)]
    use_case = ListTodosUseCase(repository)
    todos = await use_case.execute()
    assert len(todos) == 1
    assert todos[0].title == "Test"

@pytest.mark.asyncio
async def test_update_todo_use_case():
    repository = AsyncMock()
    repository.update.return_value = Todo(id=1, title="Updated", description="Updated Desc", completed=True, created_at=None)
    use_case = UpdateTodoUseCase(repository)
    todo = Todo(id=1, title="Updated", description="Updated Desc", completed=True, created_at=None)
    updated_todo = await use_case.execute(todo)
    assert updated_todo.title == "Updated"
    assert updated_todo.completed is True

@pytest.mark.asyncio
async def test_delete_todo_use_case():
    repository = AsyncMock()
    repository.delete.return_value = None
    use_case = DeleteTodoUseCase(repository)
    await use_case.execute(1)
    repository.delete.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_delete_todo_use_case_not_found():
    repository = AsyncMock()
    repository.delete.side_effect = ValueError("Todo not found")
    use_case = DeleteTodoUseCase(repository)
    with pytest.raises(ValueError, match="Todo not found"):
        await use_case.execute(9999)