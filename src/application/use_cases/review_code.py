from pydantic import BaseModel

from core.interfaces.llm_service import ILLMService


class FullReviewCodeCommand(BaseModel):
    code: str


class FullReviewCodeUseCase:
    def __init__(self, llm_service: ILLMService):
        self._llm_service = llm_service

    def execute(self, command: FullReviewCodeCommand) -> str:
        return self._llm_service.full_code_review_response(code=command.code)
