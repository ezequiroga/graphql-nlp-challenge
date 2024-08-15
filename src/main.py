from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.openapi.utils import get_openapi

from .routers import graphql_router
from .routers import npl_router
from .config.envs import Envs
from .config.logging import setup_logging

Envs.load()
setup_logging()

app = FastAPI(
    title="API Products Documentation",
    description="This api allow you to interact to get information about products using GraphQL and NLP. The documentation for GraphQL can be found [/graphql-docs](/graphql-docs).",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphql_router.graphql_app, prefix="/graphql")
app.include_router(graphql_router.router)
app.include_router(npl_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
