from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "LinkedIn Insights Service"

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    DATABASE_URL: str

    class Config:
        env_file = ".env"
        extra = "ignore"   # 🔥 THIS LINE FIXES THE ERROR


settings = Settings()
