from unittest.mock import Mock

import pytest

from core.interfaces.code_analyzer import ICodeAnalyzer
from domain.services.code_analyzer import CodeAnalyzerService
from infra.langchain.llm_provider import LangChainLLMProvider


def llm_service(): ...


@pytest.fixture
def code_analyzer_service() -> ICodeAnalyzer:
    return CodeAnalyzerService()


def mocked_llm_provider() -> LangChainLLMProvider:
    return Mock(spec=LangChainLLMProvider)
