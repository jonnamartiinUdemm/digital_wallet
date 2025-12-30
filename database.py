from sqlmodel import SQLModel, create_engine, Session
from settings import settings

connection_string = settings.database_url

connect_args = {}

if connection_string.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(connection_string, echo=True, connect_args=connect_args)

def create_all_tables():
    max_retries = 10      # Intentar 10 veces
    wait_seconds = 2      # Esperar 2 segundos entre intentos

    for i in range(max_retries):
        try:
            print(f"🔄 Intentando conectar a la DB (Intento {i+1}/{max_retries})...")
            SQLModel.metadata.create_all(engine)
            print("✅ Conexión exitosa. Tablas creadas.")
            return  
        except OperationalError:
            print(f"⏳ La base de datos no está lista. Esperando {wait_seconds}s...")
            time.sleep(wait_seconds)
    
    # Si llega aquí, falló todas las veces
    print("❌ Error crítico: No se pudo conectar a la base de datos después de varios intentos.")
    raise Exception("Database Connection Failed")
def get_session():
    with Session(engine) as session:
        yield session
