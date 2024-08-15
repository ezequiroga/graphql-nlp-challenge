from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth_router
from .config.logging import setup_logging

setup_logging()

app = FastAPI(
    title="API for login and token validation",
    description="This API allows you to login and validate tokens",
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

app.include_router(auth_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
