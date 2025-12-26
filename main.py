from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends  # <--- Importa Depends
from sqlmodel import SQLModel, select, Session  # <--- Importa Session aquí también
from database import engine, get_session  # <--- Traemos get_session
from models import Movimiento

app = FastAPI()


# --- EVENTOS ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lo que pasa ANTES de que el servidor arranque
    SQLModel.metadata.create_all(engine)
    print("✅ Tablas creadas (Modo Lifespan)")
    yield


# --- RUTAS ---
@app.get("/")
def home():
    return {"status": "Online", "version": "Billetera Local 1.0"}


@app.post("/movimientos/")
def crear_movimiento(movimiento: Movimiento, session: Session = Depends(get_session)):
    session.add(movimiento)
    session.commit()
    session.refresh(movimiento)
    return movimiento


@app.get("/movimientos/")
def leer_movimientos(session: Session = Depends(get_session)):
    consulta = select(Movimiento)
    return session.exec(consulta).all()


@app.get("/saldo")
def ver_saldo(session: Session = Depends(get_session)):
    movimientos = session.exec(select(Movimiento)).all()

    saldo = 0
    for mov in movimientos:
        if mov.tipo == "ingreso":
            saldo += mov.monto
        elif mov.tipo == "gasto":
            saldo -= mov.monto

    return {"saldo_actual": saldo, "moneda": "ARS"}
