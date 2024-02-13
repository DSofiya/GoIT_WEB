from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    db_name: str
    db_host: str
    db_port: int
    email_host: str
    email_port: int
    email_starttls: bool
    email_use_ssl: bool
    email_use_tls: bool
    email_host_user: str
    email_host_password: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()