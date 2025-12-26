from sqlmodel import SQLModel, Field


# Solo definimos la clase.
class Movimiento(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    monto: float
    tipo: str
    concepto: str
