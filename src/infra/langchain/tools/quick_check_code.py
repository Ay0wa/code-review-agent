from core.interfaces.code_analyzer import ICodeAnalyzer
from core.interfaces.tool import ITool
from domain.entities.code_review import Severity
from infra.langchain.code_report_generator import CodeReportGenerator


class QuickCheckCodeTool(ITool):
    def __init__(self, code_analyzer: ICodeAnalyzer):
        self._code_analyzer = code_analyzer

    def execute(self, code: str) -> str:
        syntax_issues = self._code_analyzer.analyze_syntax(code)
        critical_smells = [
            issue
            for issue in self._code_analyzer.detect_smells(code)
            if issue.severity == Severity.CRITICAL
        ]

        return CodeReportGenerator.generate_quick_report(syntax_issues, critical_smells)
