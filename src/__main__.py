import sys
from datetime import datetime

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config.app import AppSettings
from src.core.container import Container
from src.presentation.api.router import setup_routes

app = FastAPI(
    title="AI Code Reviewer", description="API для ревью Python кода", version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = setup_routes()


@app.get("/")
async def root():
    return {
        "service": app.title,
        "version": app.version,
        "description": app.description,
        "status": "running",
        "timestamp": datetime.now().isoformat(),
    }


app.include_router(router=router)


if __name__ == "__main__":
    container = Container()
    container.wire(modules=["src.presentation.api.v1.code_review"])
    app_settings = AppSettings()
    uvicorn.run(
        app=app,
        **app_settings.model_dump(),
    )
