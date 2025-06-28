from fastapi import APIRouter

from presentation.api.v1.code_review import router as code_review_router


def setup_routes() -> APIRouter:
    router = APIRouter(prefix="/api")
    router.include_router(router=code_review_router)
    return router
