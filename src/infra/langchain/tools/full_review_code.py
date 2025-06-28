from typing import List

from core.interfaces.code_analyzer import ICodeAnalyzer
from core.interfaces.tool import ITool
from domain.entities.code_review import Issue, Severity
from infra.langchain.code_report_generator import CodeReportGenerator


class FullReviewCodeTool(ITool):
    def __init__(self, code_analyzer: ICodeAnalyzer):
        self._code_analyzer = code_analyzer

    def execute(self, code: str) -> str:
        issues = self._collect_all_issues(code)
        improvements = self._code_analyzer.suggest_improvements(code)

        score = self._calculate_score(issues)
        status = self._determine_status(score, issues)

        return CodeReportGenerator.generate_full_report(
            issues, improvements, score, status
        )

    def _collect_all_issues(self, code: str) -> List[Issue]:
        issues = []
        issues.extend(self._code_analyzer.analyze_syntax(code))
        issues.extend(self._code_analyzer.check_style(code))
        issues.extend(self._code_analyzer.detect_smells(code))
        return issues

    def _calculate_score(self, issues: List[Issue]) -> int:
        score = 10
        for issue in issues:
            if issue.severity == Severity.CRITICAL:
                score -= 3
            elif issue.severity == Severity.WARNING:
                score -= 1
        return max(0, score)

    def _determine_status(self, score: int, issues: List[Issue]) -> str:
        if any(issue.severity == Severity.CRITICAL for issue in issues):
            return "КРИТИЧНО"
        elif score >= 8:
            return "ОТЛИЧНО"
        elif score >= 6:
            return "ХОРОШО"
        else:
            return "ТРЕБУЕТ ДОРАБОТКИ"
