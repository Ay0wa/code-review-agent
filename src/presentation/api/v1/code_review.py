from datetime import datetime
from typing import Any, Dict

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from src.application.use_cases.compare_versions import (CompareVersionsCommand,
                                                        CompareVersionsUseCase)
from src.application.use_cases.explain_issue import (ExplainIssueCommand,
                                                     ExplainIssueUseCase)
from src.application.use_cases.quick_check import (QuickCheckCommand,
                                                   QuickCheckUseCase)
from src.application.use_cases.review_code import (ReviewCodeCommand,
                                                   ReviewCodeUseCase)
from src.core.container import Container

router = APIRouter(prefix="/v1/code-review", tags=["code-review"])


class ReviewRequest(BaseModel):
    code: str = Field(..., min_length=1, description="Python код для анализа")
    context: str = Field("", description="Дополнительный контекст")
    format: str = Field("detailed", description="Формат отчета")


class QuickCheckRequest(BaseModel):
    code: str = Field(..., min_length=1, description="Python код для быстрой проверки")


class ExplainIssueRequest(BaseModel):
    code: str = Field(..., min_length=1, description="Python код с проблемой")
    issue_description: str = Field(..., min_length=1, description="Описание проблемы")


class CompareVersionsRequest(BaseModel):
    original_code: str = Field(
        ..., min_length=1, description="Оригинальная версия кода"
    )
    improved_code: str = Field(..., min_length=1, description="Улучшенная версия кода")


class ApiResponse(BaseModel):
    success: bool
    data: Dict[str, Any] | None = None
    error: str | None = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


@router.post("/review", response_model=ApiResponse)
@inject
def review_code(
    request: ReviewRequest,
    use_case: ReviewCodeUseCase = Depends(Provide[Container.review_code_use_case]),
) -> ApiResponse:
    """Полное ревью Python кода с детальным анализом"""
    try:
        command = ReviewCodeCommand(
            code=request.code, context=request.context, format=request.format
        )

        result = use_case.execute(command)

        return ApiResponse(
            success=True,
            data={
                "score": result.score,
                "status": result.status,
                "issues_count": len(result.issues),
                "critical_issues": result.critical_issues_count,
                "improvements_count": len(result.improvements),
                "issues": [
                    {
                        "description": issue.description,
                        "severity": issue.severity.value,
                        "type": issue.issue_type.value,
                        "line": issue.line_number,
                        "suggestion": issue.suggestion,
                    }
                    for issue in result.issues
                ],
                "improvements": [
                    {
                        "description": imp.description,
                        "category": imp.category,
                        "priority": imp.priority,
                    }
                    for imp in result.improvements
                ],
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка анализа: {str(e)}")


@router.post("/quick-check", response_model=ApiResponse)
@inject
def quick_check(
    request: QuickCheckRequest,
    use_case: QuickCheckUseCase = Depends(Provide[Container.quick_check_use_case]),
) -> ApiResponse:
    """Быстрая проверка кода на критичные проблемы"""
    try:
        command = QuickCheckCommand(code=request.code)
        result = use_case.execute(command)

        return ApiResponse(success=True, data=result)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка быстрой проверки: {str(e)}"
        )


@router.post("/explain", response_model=ApiResponse)
@inject
def explain_issue(
    request: ExplainIssueRequest,
    use_case: ExplainIssueUseCase = Depends(Provide[Container.explain_issue_use_case]),
) -> ApiResponse:
    """Объяснение конкретной проблемы в коде"""
    try:
        command = ExplainIssueCommand(
            code=request.code, issue_description=request.issue_description
        )

        result = use_case.execute(command)

        return ApiResponse(success=True, data={"explanation": result})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка объяснения: {str(e)}")


@router.post("/compare", response_model=ApiResponse)
@inject
def compare_versions(
    request: CompareVersionsRequest,
    use_case: CompareVersionsUseCase = Depends(
        Provide[Container.compare_versions_use_case]
    ),
) -> ApiResponse:
    """Сравнение двух версий кода"""
    try:
        command = CompareVersionsCommand(
            original_code=request.original_code, improved_code=request.improved_code
        )

        result = use_case.execute(command)

        return ApiResponse(success=True, data={"comparison": result})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сравнения: {str(e)}")


@router.get("/health")
def health_check() -> Dict[str, Any]:
    """Проверка состояния сервиса ревью кода"""
    return {
        "service": "code-review",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
    }
