from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMSettings(BaseSettings):
    openai_api_key: str = "example_key"
    openai_model: str = "gpt-3.5-turbo"
    temperature: float = 0.1
    max_tokens: int = 2000
    verbose: bool = True

    model_config = SettingsConfigDict(env_prefix="LLM_")
