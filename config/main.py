from dynaconf import Dynaconf
from pydantic import BaseModel


class RedisConfig(BaseModel):
    host: str
    port: int
    db: int

class AppConfig(BaseModel):
    cache_ttl: int

class Settings(BaseModel):
    redis: RedisConfig
    app: AppConfig


env_settings = Dynaconf(settings_file=["settings.yml"])

settings = Settings(redis=env_settings["redis"],
                    app=env_settings["app"])