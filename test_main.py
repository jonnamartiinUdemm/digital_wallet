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
# TEST 3: Verificar creación de un movimiento con monto excesivo
def test_crear_movimiento_monto_excesivo():
    movimiento_data = {
        "monto": 600000,  # Monto excesivo
        "tipo": "egreso",
        "concepto": "Prueba monto alto"
    }
    response = client.post("/movimientos/", json=movimiento_data)
    assert response.status_code == 400  # Esperamos un error 400
    assert response.json() == {"detail": "Monto excede el límite de seguridad."}