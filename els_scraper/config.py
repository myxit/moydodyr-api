from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    els_url: str
    els_username: str
    els_password: str

    model_config = SettingsConfigDict(env_file='.env.local', env_file_encoding='utf-8')


def get_settings():
    return Settings()

