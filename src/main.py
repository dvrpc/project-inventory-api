from fastapi import FastAPI, Request
from .api import api_router
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import logging 

app = FastAPI()

app.include_router(api_router)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")
log = logging.getLogger(__name__)

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request: Request, exc: IntegrityError):
    error_message = str(exc.orig)
    log.error(error_message)


    if "ORA-02290" in error_message:
        return JSONResponse(
            status_code=422,
            content={"detail": "Check constraint violated"},
        )
    
    if "ORA-02291" in error_message:
        return JSONResponse(
            status_code=422,
            content={"detail": "Foreign key value has no matching primary key value"},
        )

    if "ORA-00001" in error_message:
        return JSONResponse(
            status_code=422,
            content={"detail": "Duplicate value violates unique constraint."},
        )
    
    if "ORA-01791" in error_message:
        return JSONResponse(
            status_code=422,
            content={"detail": "Incorrect ORDER BY clause."},
        )

    return JSONResponse(
        status_code=400,
        content={"detail": "Database integrity error."},
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    error = exc._message()
    log.error(error)
    return JSONResponse(
        status_code=500,
        content={"detail": "Database error."},
    )

@app.get("/")
def read_root():
    return {"Hello": "World"}