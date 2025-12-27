from pydantic import BaseModel


# 1. ESQUEMA BASE (Lo que tienen en común)
class MovimientoBase(BaseModel):
    monto: float
    tipo: str
    concepto: str


# 2. ESQUEMA DE CREACIÓN (Lo que pedimos al usuario)
# Hereda de Base. Aquí podrías poner validaciones extra si quisieras.
class MovimientoCreate(MovimientoBase):
    pass


# 3. ESQUEMA DE LECTURA (Lo que mostramos al usuario)
# Hereda de Base y AGREGA el ID (que el usuario no envía, pero nosotros sí mostramos)
class MovimientoResponse(MovimientoBase):
    id: int

    # Esta configuración le permite a Pydantic leer datos desde una clase SQLModel (Diferencia entre diccionario y objeto)
    class Config:
        from_attributes = True
