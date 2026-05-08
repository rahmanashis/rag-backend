import logging
import os

from dotenv import load_dotenv

try:
    import redis
except ImportError:  # pragma: no cover - handled at runtime
    redis = None


load_dotenv()

logger = logging.getLogger(__name__)
_redis_client = None


def get_redis_client():
    global _redis_client

    if _redis_client is not None:
        return _redis_client

    if redis is None:
        logger.warning("Redis package not installed; caching disabled")
        return None

    redis_url = os.getenv("REDIS_URL")
    socket_connect_timeout = float(os.getenv("REDIS_SOCKET_CONNECT_TIMEOUT", "1"))
    socket_timeout = float(os.getenv("REDIS_SOCKET_TIMEOUT", "1"))

    try:
        if redis_url:
            _redis_client = redis.Redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=socket_connect_timeout,
                socket_timeout=socket_timeout,
            )
        else:
            _redis_client = redis.Redis(
                host=os.getenv("REDIS_HOST", "localhost"),
                port=int(os.getenv("REDIS_PORT", "6379")),
                db=int(os.getenv("REDIS_DB", "0")),
                password=os.getenv("REDIS_PASSWORD") or None,
                decode_responses=True,
                socket_connect_timeout=socket_connect_timeout,
                socket_timeout=socket_timeout,
            )
        return _redis_client
    except Exception as e:
        logger.warning("Redis client initialization failed: %s", e)
        return None
