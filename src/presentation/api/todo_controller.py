from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from domain.entities.todo import Todo
from domain.use_cases.create_todo import CreateTodoUseCase
from domain.use_cases.get_todo import GetTodoUseCase
from domain.use_cases.list_todos import  ListTodosUseCase
from domain.use_cases.update_todo import UpdateTodoUseCase
from domain.use_cases.delete_todo import DeleteTodoUseCase
from domain.repositories.todo_repository import TodoRepository
from presentation.dependencies import get_todo_repository


router = APIRouter()

class TodoCreate(BaseModel): 
    title: str
    description: str

class TodoUpdate(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

class TodoResponse(BaseModel): 
    id: int
    title: str
    description: str
    completed: bool
    created_at: str


@router.post("/todos", response_model= TodoResponse)
async def create_todo(
    todo: TodoCreate, 
    repository: TodoRepository = Depends(get_todo_repository)
): 
    create_use_case = CreateTodoUseCase(repository)
    result = await create_use_case.execute(todo.title, todo.description)

    return TodoResponse(
        id = result.id,
        title = result.title,
        description = result.description, 
        completed = result.completed, 
        created_at = result.created_at.isoformat(),
        )


@router.get("/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: int, 
    repository: TodoRepository = Depends(get_todo_repository)
): 
    get_use_case= GetTodoUseCase(repository)
    result = await get_use_case.execute(todo_id)

    if not result: 
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return TodoResponse(
        id = result.id,
        title = result.title,
        description = result.description, 
        completed = result.completed, 
        created_at = result.created_at.isoformat(),
    )


@router.get("/todos", response_model=List[TodoResponse])
async def list_todo(
    repository: TodoRepository = Depends(get_todo_repository)
): 
    
    list_use_case = ListTodosUseCase(repository)
    result = await list_use_case.execute()
    
    return [
        TodoResponse(
        id = todo.id,
        title = todo.title,
        description = todo.description, 
        completed = todo.completed, 
        created_at = todo.created_at.isoformat(),
        ) for todo in result
    ]

@router.put("/todos", response_model=TodoResponse)
async def update_todo(
    todo: TodoUpdate,
    repository: TodoRepository = Depends(get_todo_repository)
): 
    
    update_use_case = UpdateTodoUseCase(repository)
    result = await update_use_case.execute(
        Todo(
            id=todo.id, 
            title=todo.title, 
            description= todo.description,
            completed= todo.completed, 
            created_at= None 
        )
    )

    return TodoResponse(
        id = result.id,
        title = result.title,
        description = result.description, 
        completed = result.completed, 
        created_at = result.created_at.isoformat(),
    )

@router.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(
    todo_id: int, 
    repository: TodoRepository = Depends(get_todo_repository)
    ): 

    delete_use_case = DeleteTodoUseCase(repository)

    try: 
        await delete_use_case.execute(todo_id)
    
    except ValueError as e: 
        raise HTTPException(status_code=404, detail=str(e))
    
    return "Eliminado"