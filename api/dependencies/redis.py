from typing import Any, Annotated

from redis.asyncio import ConnectionPool

from fastapi.params import Depends

from config.main import settings

cfg = settings.redis

connection_pool = ConnectionPool(host=cfg.host, port=cfg.port, db=cfg.db)

async def get_redis():
    return connection_pool.get_connection()


redis_deps = Annotated[Any, Depends(get_redis)]
