from pydantic import BaseModel

from src.domain.entities.code_review import CodeReview
from src.domain.services.llm_service import LLMService


class ReviewCodeCommand(BaseModel):
    code: str
    context: str = ""
    format: str = "detailed"


class ReviewCodeUseCase:
    def __init__(self, llm_service: LLMService):
        self._llm_service = llm_service

    def execute(self, command: ReviewCodeCommand) -> CodeReview:
        return self._llm_service.review_code(code=command.code, context=command.context)
