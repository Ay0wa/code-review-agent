from pydantic_settings import BaseSettings, SettingsConfigDict


class HTTPSettings(BaseSettings):
    proxy: str = "http://example_user:example_pass@ip:port"
    timeout: float = 30.0

    model_config = SettingsConfigDict(env_prefix="HTTP_")
