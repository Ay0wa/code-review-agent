from pydantic import BaseModel

from src.domain.services.llm_service import LLMService


class CompareVersionsCommand(BaseModel):
    original_code: str
    improved_code: str


class CompareVersionsUseCase:
    def __init__(self, llm_service: LLMService):
        self._llm_service = llm_service

    def execute(self, command: CompareVersionsCommand) -> str:
        return self._llm_service.compare_versions(
            original=command.original_code, improved=command.improved_code
        )
