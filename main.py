from fastapi import FastAPI

from src.tasks.router import task_routes
from src.user.router import user_routes


app = FastAPI(
    title="Task Management API",
    version="1.0.0",
)

app.include_router(task_routes)
app.include_router(user_routes)