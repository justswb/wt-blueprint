from fastapi import FastAPI

from .routers.api import project, task

app = FastAPI()

app.include_router(project.router)
app.include_router(task.router)


@app.get('/')
async def root():
    return {'message': 'Hello from app'}
