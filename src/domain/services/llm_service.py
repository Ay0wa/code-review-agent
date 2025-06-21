from datetime import datetime
from typing import Any, Dict

from src.core.interfaces.llm_service import ILLMService
from src.domain.entities.code_review import CodeReview, Severity
from src.domain.services.code_analyzer import CodeAnalyzerService
from src.infra.langchain.llm_provider import LangChainLLMProvider


class LLMService(ILLMService):
    def __init__(
        self, code_analyzer: CodeAnalyzerService, executor: LangChainLLMProvider
    ):
        self._code_analyzer = code_analyzer
        self._executor = executor._executor

    def review_code(self, code: str, context: str = "") -> CodeReview:
        issues = []
        improvements = []

        syntax_issues = self._code_analyzer.analyze_syntax(code)
        style_issues = self._code_analyzer.check_style(code)
        smell_issues = self._code_analyzer.detect_smells(code)
        code_improvements = self._code_analyzer.suggest_improvements(code)

        issues.extend(syntax_issues)
        issues.extend(style_issues)
        issues.extend(smell_issues)
        improvements.extend(code_improvements)

        score = self._calculate_score(issues)
        status = self._determine_status(score, issues)

        return CodeReview(
            code=code,
            context=context,
            issues=issues,
            improvements=improvements,
            score=score,
            status=status,
            timestamp=datetime.now(),
        )

    def quick_check(self, code: str) -> Dict[str, Any]:
        syntax_issues = self._code_analyzer.analyze_syntax(code)
        critical_smells = [
            issue
            for issue in self._code_analyzer.detect_smells(code)
            if issue.severity == Severity.CRITICAL
        ]

        total_critical = len(syntax_issues) + len(critical_smells)

        return {
            "critical_issues": total_critical,
            "has_syntax_errors": len(syntax_issues) > 0,
            "security_issues": len(
                [i for i in critical_smells if i.issue_type.value == "security"]
            ),
            "quick_status": "fail" if total_critical > 0 else "pass",
        }

    def explain_issue(self, code: str, issue: str) -> str:
        prompt = f"""
        Объясни проблему в коде: {issue}
        
        Код:
        ```python
        {code}
        ```
        
        Дай краткое объяснение проблемы и способ исправления.
        """

        try:
            result = self._executor.invoke({"input": prompt})
            return result["output"]
        except Exception as e:
            return f"Ошибка объяснения: {str(e)}"

    def compare_versions(self, original: str, improved: str) -> str:
        prompt = f"""
        Сравни две версии кода:
        
        Оригинал:
        ```python
        {original}
        ```
        
        Улучшенная версия:
        ```python
        {improved}
        ```
        
        Оцени улучшения.
        """

        try:
            result = self._executor.invoke({"input": prompt})
            return result["output"]
        except Exception as e:
            return f"Ошибка сравнения: {str(e)}"

    def _calculate_score(self, issues) -> int:
        score = 10
        for issue in issues:
            if issue.severity == Severity.CRITICAL:
                score -= 3
            elif issue.severity == Severity.WARNING:
                score -= 1
        return max(0, score)

    def _determine_status(self, score: int, issues) -> str:
        if any(issue.severity == Severity.CRITICAL for issue in issues):
            return "КРИТИЧНО"
        elif score >= 8:
            return "ОТЛИЧНО"
        elif score >= 6:
            return "ХОРОШО"
        else:
            return "ТРЕБУЕТ ДОРАБОТКИ"
