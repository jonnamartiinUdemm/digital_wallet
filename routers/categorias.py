from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from database import get_session
from models import Categoria, User
from schemas import CategoriaCreate, CategoriaResponse
from routers.auth import get_current_user


router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)

@router.post("/", response_model=CategoriaResponse)
def crear_categoria(categoria: CategoriaCreate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    nueva_categoria = Categoria.model_validate(categoria)
    session.add(nueva_categoria)
    session.commit()
    session.refresh(nueva_categoria)
    return nueva_categoria

@router.get("/", response_model=list[CategoriaResponse])
def leer_categorias(session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    consulta = select(Categoria)
    return session.exec(consulta).all()

# @router.delete("/{categoria_id}", response_model=dict)
# def eliminar_categoria(categoria_id: int, session: Session = Depends(get_session)):
#     categoria = session.get(Categoria, categoria_id)
#     if not categoria:
#         return {"detail": "Categoría no encontrada."}
#     session.delete(categoria)
#     session.commit()
#     return {"detail": "Categoría eliminada exitosamente."}