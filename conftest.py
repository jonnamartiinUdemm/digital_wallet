import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from main import app, get_session
from sqlalchemy.pool import StaticPool

@pytest.fixture(name="session")
def session_fixture():
    # Crear una base de datos en memoria para pruebas
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
@pytest.fixture(name="client")
def client_fixture(session: Session):
    # Dependencia para usar la sesión de prueba
    def get_test_session():
        yield session
    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

@pytest.fixture
def categoria_test(client: TestClient):
    categoria_data = {"nombre": "Categoria Test"}
    response = client.post("/categorias/", json=categoria_data)
    return response.json()