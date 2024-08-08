from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.openapi.utils import get_openapi

from .routers import graphql_router
from .routers import npl_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphql_router.graphql_app, prefix="/graphql")
app.include_router(npl_router.router)

class DocumentationResponse(BaseModel):
    documentation: dict

@app.get("/documentation", response_model=DocumentationResponse)
def get_documentation():
    return JSONResponse(content=get_openapi(title="GraphQL API", version="1.0.0", routes=app.routes))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
