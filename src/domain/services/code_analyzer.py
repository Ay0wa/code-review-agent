import ast
import os
import subprocess
import tempfile
from typing import List

from core.interfaces.code_analyzer import ICodeAnalyzer
from domain.entities.code_review import (
    Category,
    Improvement,
    Issue,
    IssueType,
    Severity,
)

IMPROVMENT_DECS_TESTING = "Добавьте unit тесты для ваших функций"
IMPROVMENT_DECS_STYLE = "Рассмотрите использование f-strings для форматирования строк"
IMPROVMENT_DECS_TYPING = "Используйте type hints для лучшей читаемости кода"

ISSUE_SUGGEST_MANY_PARAM = "Используйте dataclass или объединяйте связанные параметры"
ISSUE_SUGGEST_ADD_LOG = "Добавьте обработку исключения или логирование"
ISSUE_SUGGEST_FIND_SOLUTION = "Найдите альтернативное решение"


class CodeAnalyzerService(ICodeAnalyzer):
    def analyze_syntax(self, code: str) -> List[Issue]:
        issues = []
        try:
            ast.parse(code)
        except SyntaxError as e:
            issues.append(
                Issue(
                    description=f"Синтаксическая ошибка в строке {e.lineno}: {e.msg}",
                    severity=Severity.CRITICAL,
                    issue_type=IssueType.SYNTAX,
                    line_number=e.lineno,
                )
            )
        return issues

    def check_style(self, code: str) -> List[Issue]:
        issues = []
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".py", delete=False
            ) as temp_file:
                temp_file.write(code)
                temp_file_path = temp_file.name

            try:
                result = self._run_flake(temp_file_path)
                if result.returncode != 0:
                    for line in result.stdout.strip().split("\n"):
                        if line.strip():
                            parts = line.split(":", 3)
                            if len(parts) >= 4:
                                line_num = int(parts[1])
                                error_code = parts[3].split()[0]
                                description = parts[3].strip()

                                issues.append(
                                    Issue(
                                        description=f"{error_code}: {description}",
                                        severity=Severity.WARNING,
                                        issue_type=IssueType.STYLE,
                                        line_number=line_num,
                                    )
                                )
            finally:
                os.unlink(temp_file_path)

        except Exception:
            pass

        return issues

    def detect_smells(self, code: str) -> List[Issue]:
        issues = []
        try:
            tree = ast.parse(code)

            for node in ast.walk(tree):
                issues_for_node = self._find_issues(node)
                issues.extend(issues_for_node)
        except Exception:
            pass

        return issues

    def suggest_improvements(self, code: str) -> List[Improvement]:
        improvements = []
        try:
            tree = ast.parse(code)

            functions_without_docs = []
            classes_without_docs = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not ast.get_docstring(node):
                        functions_without_docs.append(node.name)
                elif isinstance(node, ast.ClassDef):
                    if not ast.get_docstring(node):
                        classes_without_docs.append(node.name)

            if functions_without_docs:
                desc_func_without_docs = f"Добавьте docstrings к функциям: \
                {', '.join(functions_without_docs[:3])}"

                improvements.append(
                    Improvement(
                        description=desc_func_without_docs,
                        category=Category.DOCUMENATION,
                        priority=2,
                    )
                )

            if classes_without_docs:
                desc_class_without_docs = f"Добавьте docstrings к классам: \
                {', '.join(classes_without_docs[:3])}"
                improvements.append(
                    Improvement(
                        description=desc_class_without_docs,
                        category=Category.DOCUMENATION,
                        priority=2,
                    )
                )

            improvements.extend(
                [
                    Improvement(
                        description=IMPROVMENT_DECS_TYPING,
                        category=Category.TYPING,
                        priority=3,
                    ),
                    Improvement(
                        description=IMPROVMENT_DECS_TESTING,
                        category=Category.TESTING,
                        priority=1,
                    ),
                    Improvement(
                        description=IMPROVMENT_DECS_STYLE,
                        category=Category.STYLE,
                        priority=3,
                    ),
                ]
            )

        except Exception:
            pass

        return improvements

    @staticmethod
    def _run_flake(temp_file_path):
        return subprocess.run(
            ["flake8", "--max-line-length=88", temp_file_path],
            capture_output=True,
            text=True,
            timeout=10,
        )

    @staticmethod
    def _find_issues(node):
        issues = []
        if isinstance(node, ast.FunctionDef):
            lines_count = (node.end_lineno or 0) - node.lineno
            if lines_count > 20:
                issues.append(
                    Issue(
                        description=f"Функция '{node.name}' \
                        слишком длинная ({lines_count} строк)",
                        severity=Severity.WARNING,
                        issue_type=IssueType.SMELL,
                        line_number=node.lineno,
                        suggestion="Разбейте функцию на более мелкие части",
                    )
                )

            param_count = len(node.args.args)
            if param_count > 5:
                issues.append(
                    Issue(
                        description=f"Функция '{node.name}' \
                        имеет много параметров ({param_count})",
                        severity=Severity.WARNING,
                        issue_type=IssueType.SMELL,
                        line_number=node.lineno,
                        suggestion=ISSUE_SUGGEST_MANY_PARAM,
                    )
                )

        if isinstance(node, ast.ExceptHandler):
            if not node.body or (
                len(node.body) == 1 and isinstance(node.body[0], ast.Pass)
            ):
                issues.append(
                    Issue(
                        description="Пустой except блок",
                        severity=Severity.CRITICAL,
                        issue_type=IssueType.SMELL,
                        suggestion=ISSUE_SUGGEST_ADD_LOG,
                    )
                )

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in [
                "eval",
                "exec",
            ]:
                issues.append(
                    Issue(
                        description=f"Использование {node.func.id}() небезопасно",
                        severity=Severity.CRITICAL,
                        issue_type=IssueType.SECURITY,
                        suggestion=ISSUE_SUGGEST_FIND_SOLUTION,
                    )
                )
        return issues
