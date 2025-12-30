from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func
from typing import Optional
from datetime import datetime
from database import get_session
from models import Movimiento, Categoria, User
from schemas import MovimientoCreate, MovimientoResponse, MovimientoBase
from settings import settings
from routers.auth import get_current_user

router = APIRouter(
    prefix="/movimientos",  # Todas las rutas empezarán con /movimientos
    tags=["Movimientos"]    # Para agrupar en Swagger
)

@router.get("/saldo")
def obtener_saldo(session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    # Sumar ingresos
    ingresos = session.exec(
        select(func.sum(Movimiento.monto)).where(Movimiento.tipo == "ingreso")
    ).one() or 0.0
    
    # Sumar egresos
    egresos = session.exec(
        select(func.sum(Movimiento.monto)).where(Movimiento.tipo == "egreso")
    ).one() or 0.0
    
    return {
        "saldo_actual": ingresos - egresos,
        "ingresos_totales": ingresos,
        "egresos_totales": egresos,
        "moneda": "ARS"
    }

@router.post("/", response_model=MovimientoResponse)
def crear_movimiento(movimiento_data: MovimientoCreate, session: Session = Depends(get_session), user: User = Depends(get_current_user), saldo :float = Depends(obtener_saldo)):
    if movimiento_data.monto > settings.limite_transferencia:
        raise HTTPException(status_code=400, detail="Monto excede el límite de seguridad.")
    
    categoria = session.get(Categoria, movimiento_data.categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")
    
    if movimiento_data.tipo == "egreso" and movimiento_data.monto > saldo["saldo_actual"]:
        raise HTTPException(status_code=400, detail="Fondos insuficientes para este egreso.")
    # Exclude None para que la fecha automática funcione
    movimiento_dict = movimiento_data.model_dump(exclude_none=True)
    nuevo_movimiento = Movimiento(**movimiento_dict)
    
    session.add(nuevo_movimiento)
    session.commit()
    session.refresh(nuevo_movimiento)
    return nuevo_movimiento

@router.get("/", response_model=list[MovimientoResponse])
def leer_movimientos(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user), 
    tipo: Optional[str] = None,
    categoria_id: Optional[int] = None,
    fecha_desde: Optional[datetime] = None,
    fecha_hasta: Optional[datetime] = None,
    order_by: Optional[str] = "fecha"
):
    consulta = select(Movimiento)
    
    if tipo:
        consulta = consulta.where(Movimiento.tipo == tipo)
    if categoria_id:
        consulta = consulta.where(Movimiento.categoria_id == categoria_id)
    if fecha_desde:
        consulta = consulta.where(Movimiento.date >= fecha_desde) # Ojo: Asegúrate si tu modelo dice .date o .fecha
    if fecha_hasta:
        consulta = consulta.where(Movimiento.date <= fecha_hasta)
    
    # Ordenamiento seguro
    campos_permitidos = ["monto", "date", "concepto", "tipo"]
    if order_by not in campos_permitidos:
        order_by = "date"
        
    # Asumimos que la columna se llama 'date' en el modelo. Si es 'fecha', cámbialo aquí.
    if order_by == "fecha": order_by = "date" 
    
    columna_orden = getattr(Movimiento, order_by)
    consulta = consulta.order_by(columna_orden.desc())
    
    return session.exec(consulta).all()

@router.put("/{id}", response_model=MovimientoResponse)
def actualizar_movimiento(id: int, movimiento_data: MovimientoCreate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    movimiento_db = session.get(Movimiento, id)
    if movimiento_data.monto > settings.limite_transferencia:
        raise HTTPException(status_code=400, detail="Monto excede el límite de seguridad.")
    if not movimiento_db:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado.")
    
    movimiento_dict = movimiento_data.model_dump(exclude_none=True)
    for key, value in movimiento_dict.items():
        setattr(movimiento_db, key, value)
    
    session.add(movimiento_db)
    session.commit()
    session.refresh(movimiento_db)
    return movimiento_db

@router.delete("/{id}")
def eliminar_movimiento(id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    movimiento = session.get(Movimiento, id)
    if not movimiento:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado.")
    session.delete(movimiento)
    session.commit()
    return {"detail": "Movimiento eliminado exitosamente."}