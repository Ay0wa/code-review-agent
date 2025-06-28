from dependency_injector import containers, providers

from application.use_cases.compare_versions import CompareVersionsUseCase
from application.use_cases.explain_issue import ExplainIssueUseCase
from application.use_cases.quick_check import QuickCheckUseCase
from application.use_cases.review_code import FullReviewCodeUseCase
from core.config.llm import LLMSettings
from domain.services.code_analyzer import CodeAnalyzerService
from domain.services.llm_service import LLMService
from infra.http.http_client import get_http_client
from infra.langchain.llm_provider import LangChainLLMProvider
from infra.langchain.tools.full_review_code import FullReviewCodeTool
from infra.langchain.tools.quick_check_code import QuickCheckCodeTool


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    http_client = providers.Singleton(get_http_client)

    llm_settings = providers.Singleton(LLMSettings)

    code_analyzer_service = providers.Factory(CodeAnalyzerService)
    llm_provider = providers.Factory(
        LangChainLLMProvider, settings=llm_settings, http_client=http_client
    )

    full_review_code_tool = providers.Factory(
        FullReviewCodeTool,
        code_analyzer=code_analyzer_service,
    )
    quick_check_code_tool = providers.Factory(
        QuickCheckCodeTool,
        code_analyzer=code_analyzer_service,
    )

    llm_service = providers.Factory(
        LLMService,
        llm_provider=llm_provider,
        full_review_code_tool=full_review_code_tool,
        quick_check_code_tool=quick_check_code_tool,
    )

    review_code_use_case = providers.Factory(
        FullReviewCodeUseCase, llm_service=llm_service
    )

    quick_check_use_case = providers.Factory(QuickCheckUseCase, llm_service=llm_service)

    explain_issue_use_case = providers.Factory(
        ExplainIssueUseCase, llm_service=llm_service
    )

    compare_versions_use_case = providers.Factory(
        CompareVersionsUseCase, llm_service=llm_service
    )
