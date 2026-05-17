import redis
from django.conf import settings

_client = None


def get_redis_client() -> redis.Redis:
    global _client
    if _client is None:
        _client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
    return _client


CONFIRMATION_CODE_TTL = 5 * 60  # 5 minutes in seconds


def save_confirmation_code(email: str, code: str) -> None:
    get_redis_client().setex(f"confirm:{email}", CONFIRMATION_CODE_TTL, code)


def get_confirmation_code(email: str) -> str | None:
    return get_redis_client().get(f"confirm:{email}")


def delete_confirmation_code(email: str) -> None:
    get_redis_client().delete(f"confirm:{email}")
