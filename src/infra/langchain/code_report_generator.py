from typing import List

from domain.entities.code_review import Improvement, Issue


class CodeReportGenerator:
    @staticmethod
    def generate_full_report(
        issues: List[Issue], improvements: List[Improvement], score: int, status: str
    ) -> str:
        sections = [
            CodeReportGenerator._build_full_header(issues, score, status),
            CodeReportGenerator._build_issues_section(issues),
            CodeReportGenerator._build_improvements_section(improvements),
        ]
        return "".join(sections)

    @staticmethod
    def generate_quick_report(
        syntax_issues: List[Issue], critical_smells: List[Issue]
    ) -> str:
        total_critical = len(syntax_issues) + len(critical_smells)
        security_issues = [
            i
            for i in critical_smells
            if hasattr(i, "issue_type") and i.issue_type.value == "security"
        ]
        status = "ПРОВАЛ" if total_critical > 0 else "УСПЕХ"

        sections = [
            CodeReportGenerator._build_quick_header(
                status, total_critical, len(syntax_issues), len(security_issues)
            ),
            CodeReportGenerator._build_quick_issues_section(
                "СИНТАКСИЧЕСКИЕ ОШИБКИ", syntax_issues
            ),
            CodeReportGenerator._build_quick_issues_section(
                "КРИТИЧЕСКИЕ ПРОБЛЕМЫ", critical_smells
            ),
        ]
        return "".join(sections)

    @staticmethod
    def _build_full_header(issues: List[Issue], score: int, status: str) -> str:
        lines = [
            "РЕЗУЛЬТАТЫ АНАЛИЗА КОДА",
            "",
            f"Найдено проблем: {len(issues)}",
            f"Оценка: {score}/10",
            f"Статус: {status}",
            "",
            "",
        ]
        return "\n".join(lines)

    @staticmethod
    def _build_quick_header(
        status: str, total_critical: int, syntax_count: int, security_count: int
    ) -> str:
        lines = [
            "БЫСТРАЯ ПРОВЕРКА КОДА",
            "",
            f"Статус: {status}",
            f"Критических проблем: {total_critical}",
            f"Синтаксических ошибок: {syntax_count}",
            f"Проблем безопасности: {security_count}",
            "",
            "",
        ]
        return "\n".join(lines)

    @staticmethod
    def _build_quick_issues_section(title: str, issues: List[Issue]) -> str:
        if not issues:
            return ""

        lines = [title + ":"]
        for i, issue in enumerate(issues, 1):
            lines.append(f"{i}. {issue.description} (строка {issue.line_number})")
        lines.append("")
        return "\n".join(lines)

    @staticmethod
    def _build_issues_section(issues: List[Issue]) -> str:
        if not issues:
            return ""

        lines = ["\nНАЙДЕННЫЕ ПРОБЛЕМЫ:"]
        for i, issue in enumerate(issues, 1):
            severity_str = (
                issue.severity.value
                if hasattr(issue.severity, "value")
                else str(issue.severity)
            )
            lines.append(f"{i}. [{severity_str}] {issue.description}")
            lines.append(f"   Строка: {issue.line_number}")

            if hasattr(issue, "suggestion") and issue.suggestion:
                lines.append(f"   Рекомендация: {issue.suggestion}")
            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def _build_improvements_section(improvements: List[Improvement]) -> str:
        if not improvements:
            return ""

        lines = ["\nПРЕДЛОЖЕНИЯ ПО УЛУЧШЕНИЮ:"]
        for i, improvement in enumerate(improvements, 1):
            lines.append(f"{i}. {improvement.description}")
            if hasattr(improvement, "example") and improvement.example:
                lines.append(f"   Пример: {improvement.example}")
            lines.append("")

        return "\n".join(lines)
