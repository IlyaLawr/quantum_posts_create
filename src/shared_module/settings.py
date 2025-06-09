from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    db_url: str = Field(default=f'sqlite+aiosqlite:///{PROJECT_ROOT}/database/data.db',
                        env='DB_URL')
    db_logs: bool = False

    bot_token: str = Field(env='BOT_TOKEN')

    web_app_host: str = Field(env='WEB_APP_HOST')
    web_app_port: str = Field(env='WEB_APP_PORT')

    class Config:
        env_file = str(PROJECT_ROOT.parent / '.env')
        env_file_encoding = 'utf-8'


settings = Settings()
