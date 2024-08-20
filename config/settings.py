from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://authdb_owner:V97gEkaPchLf@ep-plain-water-a5scbycn.us-east-2.aws.neon.tech/authdb"
    secret_key: str = "empty_string"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    class Config:
        env_file = ".env"


settings = Settings()
