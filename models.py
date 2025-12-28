from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional


# Solo definimos la clase.
class Movimiento(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    monto: float
    tipo: str
    concepto: str
    categoria_id: Optional[int] = Field(default=None, foreign_key="categoria.id")
    categoria: Optional["Categoria"] = Relationship(back_populates="movimientos")

class Categoria(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    descripcion: Optional[str] = None
    movimientos: List["Movimiento"] = Relationship(back_populates="categoria")
