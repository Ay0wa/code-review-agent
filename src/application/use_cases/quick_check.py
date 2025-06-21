from typing import Any, Dict

from pydantic import BaseModel

from src.domain.services.llm_service import LLMService


class QuickCheckCommand(BaseModel):
    code: str


class QuickCheckUseCase:
    def __init__(self, llm_service: LLMService):
        self._llm_service = llm_service

    def execute(self, command: QuickCheckCommand) -> Dict[str, Any]:
        return self._llm_service.quick_check(code=command.code)
