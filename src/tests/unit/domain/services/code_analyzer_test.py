from typing import List

import pytest

from core.interfaces.code_analyzer import ICodeAnalyzer
from domain.entities.code_review import Issue, IssueType, Severity

SIMPLE_CODE_WITHOUT_EXC = "print('hello world')"
CODE_WITH_EXC = "print(/'hello world')"


def create_style_issue_w292(line_number: int):
    return Issue(
        description="W292: W292 no newline at end of file",
        severity=Severity.WARNING,
        issue_type=IssueType.STYLE,
        line_number=line_number,
    )


def test_analyze_syntax_without_issues(code_analyzer_service: ICodeAnalyzer):
    issues = code_analyzer_service.analyze_syntax(SIMPLE_CODE_WITHOUT_EXC)

    assert issues == []


def test_analyze_syntax_with_issues(code_analyzer_service: ICodeAnalyzer):
    issues = code_analyzer_service.analyze_syntax(CODE_WITH_EXC)

    expected = [
        Issue(
            description="Синтаксическая ошибка в строке 1: invalid syntax",
            severity=Severity.CRITICAL,
            issue_type=IssueType.SYNTAX,
            line_number=1,
        )
    ]

    assert issues == expected


@pytest.mark.parametrize(
    ("code", "expected"), [("print('hello world')", [create_style_issue_w292(1)])]
)
def test_check_style_without_issues(
    code_analyzer_service: ICodeAnalyzer, code: str, expected: List[Issue]
):
    issues = code_analyzer_service.check_style(code)

    assert issues == expected
