from dynaconf import Dynaconf
from pydantic import BaseModel


class RedisConfig(BaseModel):
    host: str
    port: int
    db: int



class AppConfig(BaseModel):
    redis: RedisConfig


env_settings = Dynaconf(settings_file=["settings.yml"])

settings = AppConfig(redis=env_settings["redis"])