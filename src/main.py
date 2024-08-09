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
    version="1.0.0"
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

class DocumentationResponse(BaseModel):
    documentation: dict

@app.middleware("http")
async def restrict_docs_access(request: Request, call_next):
    if request.url.path.startswith("/docs") or request.url.path.startswith("/graphql-docs"):
        internal_access_header = request.headers.get("X-Internal-Access")
        if internal_access_header != "allow-docs-access":
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "Access forbidden"})
    response = await call_next(request)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
