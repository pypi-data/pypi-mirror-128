from functools import lru_cache
from os import getenv

from pydantic import BaseSettings


class UvicornSettings(BaseSettings):
    app: str = getenv("CHAT_APP", "chat.app:app")
    host: str = getenv("CHAT_HOST", "0.0.0.0")
    port: int = getenv("CHAT_PORT", 8088)
    workers: int = getenv("CHAT_WORKERS", 1)
    reload: bool = getenv("CHAT_RELOAD", True)
    log_level: str = getenv("CHAT_LOG_LEVEL", "info")


class BrokerSettings(BaseSettings):
    host: str = getenv("CHAT_BROKER_HOST", "0.0.0.0")
    port: int = getenv("CHAT_BROKER_PORT", 6300)
    db: int = getenv("CHAT_BROKER_DB", 2)
    channel_name: str = getenv("CHAT_CHANNEL_NAME", "chat_channel")


class DjangoServerSettings(BaseSettings):
    base_url: str = getenv("CHAT_DJANGO_BASE_URL", "http://localhost:4114/")
    get_user_url: str = base_url + getenv(
        "CHAT_DJANGO_GET_USER_URL", "api/v1/me/"
    )
    token_type: str = getenv("CHAT_DJANGO_TOKEN_TYPE", "Bearer")
    user_response_id_field: str = getenv(
        "CHAT_DJANGO_USER_RESPONSE_ID_FIELD", "id"
    )


class GlobalSettings(BaseSettings):
    sentry_dsn: str = getenv(
        "CHAT_SENTRY_DSN",
        "https://f297e4c4d8854da893b1c679625e6768@o917775.ingest.sentry.io/6075514",
    )
    environment: str = getenv("CHAT_SENTRY_ENV", "chat")
    capture_messages: bool = getenv("CHAT_SENTRY_CAPTURE_MESSAGES", True)


@lru_cache
def get_global_settings():
    return GlobalSettings()


@lru_cache
def get_django_settings():
    return DjangoServerSettings()


@lru_cache
def get_broker_settings():
    return BrokerSettings()
