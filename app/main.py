from http import HTTPStatus

from fastapi import FastAPI, Request, HTTPException

from .routers.api import project

app = FastAPI()

app.include_router(project.router)


@app.get('/')
async def root():
    return {'message': 'Hello from app'}

@app.exception_handler(AssertionError)
async def assertion_error_handler(req: Request, exc: AssertionError):
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=exc.args)
