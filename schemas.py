from pydantic import BaseModel, ConfigDict
from datetime import datetime

#Categorias
class CategoriaBase(BaseModel):
    nombre: str

class CategoriaCreate(CategoriaBase):
    pass
class CategoriaResponse(CategoriaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
# Movimientos
class MovimientoBase(BaseModel):
    monto: float
    tipo: str
    concepto: str
    date: datetime | None = None

# 2. ESQUEMA DE CREACIÓN (Lo que pedimos al usuario)
class MovimientoCreate(MovimientoBase):
    categoria_id: int


# 3. ESQUEMA DE LECTURA (Lo que mostramos al usuario)
class MovimientoResponse(MovimientoBase):
    id: int
    categoria: CategoriaResponse | None = None
    # Esta configuración le permite a Pydantic leer datos desde una clase SQLModel (Diferencia entre diccionario y objeto)
    model_config = ConfigDict(from_attributes=True)
    date: datetime
    categoria_id: int

#Usuarios

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
    
class Token(BaseModel):
    access_token: str
    token_type: str