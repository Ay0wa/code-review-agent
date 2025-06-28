import httpx
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from core.config.llm import LLMSettings


class ExecutorNotFoundError(Exception):
    pass


class LangChainLLMProvider:
    def __init__(self, settings: LLMSettings, http_client: httpx.Client):
        self._settings = settings
        self._executor = None
        self._llm = ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=settings.temperature,
            http_client=http_client,
        )

    @property
    def executor(self) -> AgentExecutor:
        """Возвращает executor, если он существует"""
        if self._executor is None:
            raise ExecutorNotFoundError(
                "Executor не инициализирован. Вызовите setup_agent() сначала."
            )
        return self._executor

    def get_llm(self) -> ChatOpenAI:
        """Возвращает настроенную LLM модель"""
        return self._llm

    def setup_agent(self, tools):
        """Настраивает агента с переданными инструментами"""
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Ты опытный Python разработчик и ментор.
            Задачи, которые придется выполнять:
            
                - Полное ревью кода, используя tool: full_review_code_tool
                - Быстрое ревью кода, используя tool: quick_check_tool
                - На выходе ты должен выдать идеально-чистый исправленный код
                
            Анализируй код конструктивно и давай полезные советы.
            
            Всегда используй соответствующие инструменты для анализа кода перед тем, 
            как давать рекомендации или исправления.""",
                ),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )

        agent = create_openai_tools_agent(self._llm, tools, prompt)
        self._executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=self._settings.verbose,
            return_intermediate_steps=True,
        )
