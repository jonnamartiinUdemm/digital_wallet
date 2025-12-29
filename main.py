from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_all_tables
from routers import movimientos, categorias # Importamos los nuevos archivos

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_all_tables()
    print("✅ Tablas creadas y App lista")
    yield


app = FastAPI(lifespan=lifespan, title="Billetera Local", version="2.0")

# --- CONECTAMOS LOS ROUTERS ---
app.include_router(movimientos.router)
app.include_router(categorias.router)

@app.get("/")
def read_root():
    return {"status": "Online", "version": "Billetera Local 2.0 (Refactorizada)"}