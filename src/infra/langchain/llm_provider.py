import httpx
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate
from langchain.tools import tool
from langchain_openai import ChatOpenAI

from src.core.config.llm import LLMSettings


class LangChainLLMProvider:
    def __init__(self, settings: LLMSettings, http_client: httpx.Client):
        self._settings = settings
        self._llm = ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
            http_client=http_client,
        )
        self._setup_agent()

    def _setup_agent(self):
        @tool
        def analyze_code_structure(code: str) -> str:
            """Анализирует структуру Python кода"""
            return f"Анализ структуры для кода длиной {len(code)} символов"

        @tool
        def generate_report(issues_count: int, score: int) -> str:
            """Генерирует финальный отчет"""
            return f"Отчет: найдено {issues_count} проблем, оценка {score}/10"

        tools = [analyze_code_structure, generate_report]

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Ты опытный Python разработчик и ментор. 
            Анализируй код конструктивно и давай полезные советы.""",
                ),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )

        agent = create_openai_tools_agent(self._llm, tools, prompt)
        self._executor = AgentExecutor(
            agent=agent, tools=tools, verbose=self._settings.verbose
        )
