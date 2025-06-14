from datetime import datetime

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config.app import AppSettings

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


@app.get("/")
async def root():
    return {
        "service": app.title,
        "version": app.version,
        "description": app.description,
        "status": "running",
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    app_settings = AppSettings()
    uvicorn.run(
        app=app,
        **app_settings.model_dump(),
    )
