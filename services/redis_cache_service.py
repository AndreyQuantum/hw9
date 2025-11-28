import inspect
import json
import functools
from typing import Callable, Any, Awaitable

from fastapi.encoders import jsonable_encoder
from redis.asyncio import ConnectionPool, Connection, Redis
from config.main import settings
from fastapi import Request


class RedisCache:
    cfg = settings.redis

    connection_pool = ConnectionPool(host=cfg.host, port=cfg.port, db=cfg.db)

    async def get_redis(self) -> Redis:
        return await Redis.from_pool(connection_pool=self.connection_pool)

    def _serialize(self, value: Any) -> str:
        return json.dumps(jsonable_encoder(value))

    def _deserialize(self, value: bytes | None) -> Any:
        if value is None:
            return None
        return json.loads(value)

    def _extract_request(
            self,
            func: Callable[..., Awaitable[Any]],
            args: tuple[Any, ...],
            kwargs: dict[str, Any],
    ) -> Request:
        bound = inspect.signature(func).bind_partial(*args, **kwargs)
        for v in bound.arguments.values():
            if isinstance(v, Request):
                return v
        v = bound.arguments.get("request")
        if isinstance(v, Request):
            return v
        raise ValueError("Request not found in arguments")

    def cache(self, ttl: int = settings.app.cache_ttl):
        def decorator(func: Callable[..., Awaitable[Any]]):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                request = self._extract_request(func, args, kwargs)
                key = self._make_key(request)
                redis = await self.get_redis()
                cached = await redis.get(key)
                if cached is not None:
                    print("Cache hit")
                    return self._deserialize(cached)

                result = await func(*args, **kwargs)
                await redis.set(key, self._serialize(result), ex=ttl)
                return result
            return wrapper
        return decorator

    def invalidate(self,):
        def decorator(func: Callable[..., Awaitable[Any]]):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                result = await func(*args, **kwargs)
                request = self._extract_request(func, args, kwargs)
                await self._invalidate_pattern(request.url.path.split("/")[0] + "*")
                return result
            return wrapper
        return decorator

    def _make_key(self, request: Request) -> str:
        return str(request.url)

    async def _invalidate_pattern(self, pattern: str):
        redis = await self.get_redis()
        async for key in redis.scan_iter(match=pattern):
            await redis.delete(key)
