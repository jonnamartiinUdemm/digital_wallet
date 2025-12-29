import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app
from database import get_session
from models import User, Categoria # <--- IMPORTANTE: Agregué Categoria aquí
from security import create_access_token, get_password_hash

# 1. Base de datos en memoria
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", 
        connect_args={"check_same_thread": False}, 
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

# 2. CREAR USUARIO DE PRUEBA (Para Auth)
@pytest.fixture(name="test_user")
def test_user_fixture(session: Session):
    user = User(
        username="testuser",
        email="test@test.com",
        hashed_password=get_password_hash("test1234")
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# 3. CREAR CATEGORÍA DE PRUEBA (¡RECUPERADA!)
@pytest.fixture(name="categoria_test")
def categoria_fixture(session: Session):
    categoria = Categoria(nombre="Comida", tipo="Gasto")
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria

# 4. GENERAR TOKEN
@pytest.fixture(name="auth_headers")
def auth_headers_fixture(test_user):
    access_token = create_access_token(data={"sub": test_user.username})
    return {"Authorization": f"Bearer {access_token}"}

# 5. CLIENTE AUTENTICADO
@pytest.fixture(name="client")
def client_fixture(session: Session, auth_headers):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    with TestClient(app) as client:
        # El cliente usa el token automáticamente en cada petición
        client.headers.update(auth_headers) 
        yield client
        
    app.dependency_overrides.clear()