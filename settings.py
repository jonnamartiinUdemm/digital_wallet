from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Definimos las variables que ESPERAMOS encontrar
    limite_transferencia: int
    nombre_app: str = "Billetera Local" # Valor por defecto si no está en el .env

    # Configuración para que lea el archivo .env automáticamente
    model_config = SettingsConfigDict(env_file=".env")

# Instanciamos la clase una sola vez para importarla desde otros lados
settings = Settings()