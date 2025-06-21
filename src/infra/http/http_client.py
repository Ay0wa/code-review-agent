import httpx

from src.core.config.http import HTTPSettings


def get_http_client() -> httpx.Client:
    http_settings = HTTPSettings()
    http_client = httpx.Client(**http_settings.model_dump())
    return http_client
