from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Definimos las variables que ESPERAMOS encontrar
    limite_transferencia: int
    nombre_app: str = "Billetera Local"
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

# Si no existe en el .env, usará SQLite por defecto
    database_url: str = "sqlite:///./billetera_v2.db"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
