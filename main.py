from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import select, Session
from database import engine, get_session
from models import Movimiento
from schemas import MovimientoCreate, MovimientoResponse
from settings import settings
from contextlib import asynccontextmanager


# --- EVENTOS ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lo que pasa ANTES de que el servidor arranque
    SQLModel.metadata.create_all(engine)
    print("✅ Tablas creadas (Modo Lifespan)")
    yield
    print("Hasta la proxima")


app = FastAPI(lifespan=lifespan)


# --- RUTAS ---
@app.get("/")
def home():
    return {"status": "Online", "version": "Billetera Local 1.0"}


@app.post("/movimientos/")
def crear_movimiento(
    movimiento_data: MovimientoCreate, session: Session = Depends(get_session)
):
    if movimiento_data.monto > settings.limite_transferencia:
        raise HTTPException(
            status_code=400, detail="Monto excede el límite de seguridad."
        )
    nuevo_movimiento = Movimiento(**movimiento_data.model_dump())

    session.add(nuevo_movimiento)
    session.commit()
    session.refresh(nuevo_movimiento)

    return nuevo_movimiento


@app.get("/movimientos/", response_model=list[MovimientoResponse])
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


@app.delete("/movimientos/{movimiento_id}")
def eliminar_movimiento(movimiento_id: int, session: Session = Depends(get_session)):
    movimiento = session.get(Movimiento, movimiento_id)
    if not movimiento:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado.")

    session.delete(movimiento)
    session.commit()
    return {"detail": "Movimiento eliminado exitosamente."}


@app.put("/movimientos/{movimiento_id}")
def actualizar_movimiento(
    movimiento_id: int,
    movimiento_data: MovimientoCreate,
    session: Session = Depends(get_session),
):
    movimiento = session.get(Movimiento, movimiento_id)
    if not movimiento:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado.")

    if movimiento_data.monto > settings.limite_transferencia:
        raise HTTPException(
            status_code=400, detail="Monto excede el límite de seguridad."
        )

    movimiento_dict = movimiento_data.model_dump()
    for key, value in movimiento_dict.items():
        setattr(movimiento, key, value)

    session.add(movimiento)
    session.commit()
    session.refresh(movimiento)
    return movimiento
