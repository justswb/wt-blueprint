from http import HTTPStatus

from fastapi import HTTPException

from ...runtime import require_project as _require_project


def require_project():
    try:
        return _require_project()
    except Exception as exc:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=exc.args)
