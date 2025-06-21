from dependency_injector import containers, providers

from src.application.use_cases.compare_versions import CompareVersionsUseCase
from src.application.use_cases.explain_issue import ExplainIssueUseCase
from src.application.use_cases.quick_check import QuickCheckUseCase
from src.application.use_cases.review_code import ReviewCodeUseCase
from src.core.config.llm import LLMSettings
from src.domain.services.code_analyzer import CodeAnalyzerService
from src.domain.services.llm_service import LLMService
from src.infra.http.http_client import get_http_client
from src.infra.langchain.llm_provider import LangChainLLMProvider


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    http_client = providers.Singleton(get_http_client)

    llm_settings = providers.Singleton(LLMSettings)

    code_analyzer_service = providers.Factory(CodeAnalyzerService)
    executor = providers.Factory(
        LangChainLLMProvider, settings=llm_settings, http_client=http_client
    )

    llm_service = providers.Factory(
        LLMService,
        code_analyzer=code_analyzer_service,
        executor=executor,
    )

    review_code_use_case = providers.Factory(ReviewCodeUseCase, llm_service=llm_service)

    quick_check_use_case = providers.Factory(QuickCheckUseCase, llm_service=llm_service)

    explain_issue_use_case = providers.Factory(
        ExplainIssueUseCase, llm_service=llm_service
    )

    compare_versions_use_case = providers.Factory(
        CompareVersionsUseCase, llm_service=llm_service
    )
