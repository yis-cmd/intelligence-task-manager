from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    host:str = "127.0.0.1"
    port:int = 3306
    user:str = "root"
    password:str = "1234"

    model_config = SettingsConfigDict(env_file="config.env", env_prefix="DB_")
