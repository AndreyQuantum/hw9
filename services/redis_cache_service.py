import json
import functools
from typing import Callable, Any, Awaitable
from redis.asyncio import ConnectionPool

from config.main import settings



class RedisCache:
    cfg = settings.redis

    connection_pool = ConnectionPool(host=cfg.host, port=cfg.port, db=cfg.db)

    def get_redis(self):
        return self.connection_pool.get_connection()

    def _serialize(self, value: Any) -> str:
        return json.dumps(value)

    def _deserialize(self, value: bytes | None) -> Any:
        if value is None:
            return None
        return json.loads(value)

    def cache(self, ttl: int = settings.app.cache_ttl):
        def decorator(func: Callable[..., Awaitable[Any]]):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                key = self._make_key(func.__name__, args, kwargs)
                redis = await self.get_redis()
                cached = await redis.get(key)
                if cached is not None:
                    return self._deserialize(cached)

                result = await func(*args, **kwargs)
                await redis.set(key, self._serialize(result), ex=ttl)
                return result
            return wrapper
        return decorator

    def invalidate(self, pattern: str = "get*"):
        def decorator(func: Callable[..., Awaitable[Any]]):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                result = await func(*args, **kwargs)
                await self._invalidate_pattern(pattern)
                return result
            return wrapper
        return decorator

    def _make_key(self, name: str, args: tuple, kwargs: dict) -> str:
        return f"{name}:{json.dumps(args, sort_keys=True)}:{json.dumps(kwargs, sort_keys=True)}"

    async def _invalidate_pattern(self, pattern: str):
        redis = await self.get_redis()
        async for key in redis.scan_iter(match=pattern):
            await redis.delete(key)
