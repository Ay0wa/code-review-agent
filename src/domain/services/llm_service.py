from langchain.tools import tool

from core.interfaces.llm_service import ILLMService
from infra.langchain.llm_provider import LangChainLLMProvider
from infra.langchain.tools.full_review_code import FullReviewCodeTool
from infra.langchain.tools.quick_check_code import QuickCheckCodeTool


class LLMService(ILLMService):
    def __init__(
        self,
        llm_provider: LangChainLLMProvider,
        full_review_code_tool: FullReviewCodeTool,
        quick_check_code_tool: QuickCheckCodeTool,
    ):
        self.llm_provider = llm_provider
        self.full_review_code_tool = full_review_code_tool
        self.quick_check_code_tool = quick_check_code_tool
        self._setup_agent()

    def _setup_agent(self):
        """Настраивает агента с инструментами"""

        @tool
        def full_review_code_tool(code: str) -> str:
            """Проводит полное ревью Python кода и возвращает детальный анализ.

            Args:
                code: Python код для анализа

            Returns:
                Детальный отчет с найденными проблемами, улучшениями и рекомендациями
            """
            return self.full_review_code_tool.execute(code)

        @tool
        def quick_check_tool(code: str) -> str:
            """Быстрая проверка критических проблем в коде.

            Args:
                code: Python код для быстрой проверки

            Returns:
                Краткий отчет о критических проблемах
            """
            return self.quick_check_code_tool.execute(code)

        self.llm_provider.setup_agent([full_review_code_tool, quick_check_tool])

    def full_code_review_response(self, code: str) -> str:
        """Получает ответ от LLM с использованием инструментов"""

        input_message = f"""
        Пожалуйста, проанализируй следующий Python код:
        
        ```python
        {code}
        ```
        
        1. Используй инструмент full_review_code_tool для полного анализа
        2. На основе результата анализа предоставь исправленную версию кода
        """

        try:
            result = self.llm_provider.executor.invoke({"input": input_message})

            return result["output"]

        except Exception as e:
            return f"Ошибка при анализе кода: {str(e)}"

    def quick_check_response(self, code: str) -> str:
        """Получает ответ от LLM с использованием инструментов"""

        input_message = f"""
        Пожалуйста, проанализируй следующий Python код:
        
        ```python
        {code}
        ```
        
        1. Используй инструмент quick_check_tool для быстрого анализа
        2. На основе результата анализа предоставь исправленную версию кода
        """

        try:
            result = self.llm_provider.executor.invoke({"input": input_message})

            return result["output"]

        except Exception as e:
            return f"Ошибка при анализе кода: {str(e)}"

    def explain_issue_response(self, code: str, issue: str) -> str:
        """Объясняет конкретную проблему в коде"""
        input_message = f"""
        Объясни следующую проблему в коде: {issue}
        
        Код:
        ```python
        {code}
        ```
        
        Дай краткое объяснение проблемы и способ исправления.
        """

        try:
            result = self.llm_provider.executor.invoke({"input": input_message})
            return result["output"]
        except Exception as e:
            return f"Ошибка объяснения: {str(e)}"

    def compare_versions_response(self, original: str, improved: str) -> str:
        """Сравнивает две версии кода"""
        input_message = f"""
        Сравни две версии кода:
        
        Оригинальная версия:
        ```python
        {original}
        ```
        
        Улучшенная версия:
        ```python
        {improved}
        ```
        
        Оцени улучшения и объясни разницу.
        """

        try:
            result = self.llm_provider.executor.invoke({"input": input_message})
            return result["output"]
        except Exception as e:
            return f"Ошибка сравнения: {str(e)}"
