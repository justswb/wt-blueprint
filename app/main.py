from fastapi import FastAPI

from .routers.api import project, task, relation, feature

app = FastAPI()

app.include_router(project.router)
app.include_router(task.router)
app.include_router(relation.router)
app.include_router(feature.router)


@app.get('/')
async def root():
    return {'message': 'Hello from app'}
