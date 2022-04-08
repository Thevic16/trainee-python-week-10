from fastapi import FastAPI, Request
from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel
from starlette.responses import JSONResponse

from databases.db import engine, get_db_session
from graphql_app.app import graphql_app
from resolvers import films

from utilities.logger import Logger

app = FastAPI()

session = get_db_session()

# Creating databases
SQLModel.metadata.create_all(engine)

# Add routes
app.include_router(films.router)

# GraphQL app
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)


# Handling Errors--------------------------------------------------------------
@app.exception_handler(IntegrityError)
async def integrityError_exception_handler(request: Request,
                                           exc: IntegrityError):
    Logger.error(f"Integrity Error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": f"Integrity Error: {exc.orig}"},
    )


@app.exception_handler(AttributeError)
async def attributeError_exception_handler(request: Request,
                                           exc: AttributeError):
    Logger.error(f"AttributeError: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": f"Attribute Error {exc.name}"},
    )


@app.exception_handler(TypeError)
async def NoneType_exception_handler(request: Request,
                                     exc: TypeError):
    Logger.error(f"AttributeError: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "TypeError"},
    )
