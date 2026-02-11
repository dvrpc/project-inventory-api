from fastapi import FastAPI, Request
from api import api_router
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

app = FastAPI()

app.include_router(api_router)

@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request: Request, exc: IntegrityError):
    error_message = str(exc.orig)


    if "ORA-02290" in error_message:
        return JSONResponse(
            status_code=422,
            content={"detail": "Check constraint violated"},
        )

    if "ORA-00001" in error_message:
        return JSONResponse(
            status_code=422,
            content={"detail": "Duplicate value violates unique constraint."},
        )

    return JSONResponse(
        status_code=400,
        content={"detail": "Database integrity error."},
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={"detail": "Database error."},
    )

@app.get("/")
def read_root():
    return {"Hello": "World"}