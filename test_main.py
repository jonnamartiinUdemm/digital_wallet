from fastapi.testclient import TestClient
from main import app

# Creamos un "Cliente de Prueba".
client = TestClient(app)

# TEST 1: Verificar que la ruta de inicio responde
def test_read_main():
    response = client.get("/")  # Simulamos entrar a "/"
    assert response.status_code == 200  # Esperamos código 200 (OK)
    assert response.json() == {"status": "Online", "version": "Billetera Local 1.0"}

# TEST 2: Verificar la estructura del saldo
def test_read_saldo():
    response = client.get("/saldo")
    assert response.status_code == 200
    data = response.json()

    # Validamos que la respuesta tenga las llaves correctas
    assert "saldo_actual" in data
    assert "moneda" in data
    assert data["moneda"] == "ARS"