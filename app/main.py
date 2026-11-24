from fastapi import FastAPI

from .routers.api import project

app = FastAPI()

app.include_router(project.router)


@app.get('/')
async def root():
    return {'message': 'Hello from app'}
