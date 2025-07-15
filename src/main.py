from fastapi import FastAPI
from infrastructure.database.database import Base, engine
from presentation.api.todo_controller import router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)