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
        "concepto": "Prueba monto alto",
    }
    response = client.post("/movimientos/", json=movimiento_data)
    assert response.status_code == 400  # Esperamos un error 400
    assert response.json() == {"detail": "Monto excede el límite de seguridad."}


# TEST 4: Verificar eliminación de un movimiento inexistente
def test_eliminar_movimiento_inexistente():
    response = client.delete("/movimientos/9999")  # ID que no existe
    assert response.status_code == 404  # Esperamos un error 404
    assert response.json() == {"detail": "Movimiento no encontrado."}


# TEST 5: Verificar creación y eliminación de un movimiento
def test_crear_y_eliminar_movimiento():
    movimiento_data = {
        "monto": 1000,
        "tipo": "ingreso",
        "concepto": "Prueba creación y eliminación",
    }
    # Crear el movimiento
    response_create = client.post("/movimientos/", json=movimiento_data)
    assert response_create.status_code == 200
    movimiento_creado = response_create.json()
    movimiento_id = movimiento_creado["id"]

    # Eliminar el movimiento
    response_delete = client.delete(f"/movimientos/{movimiento_id}")
    assert response_delete.status_code == 200
    assert response_delete.json() == {"detail": "Movimiento eliminado exitosamente."}


# TEST 6: Verificar actualización de un movimiento inexistente
def test_actualizar_movimiento_inexistente():
    movimiento_data = {
        "monto": 2000,
        "tipo": "egreso",
        "concepto": "Prueba actualización inexistente",
    }
    response = client.put("/movimientos/9999", json=movimiento_data)  # ID que no existe
    assert response.status_code == 404  # Esperamos un error 404
    assert response.json() == {"detail": "Movimiento no encontrado."}


# TEST 7: Verificar actualización de un movimiento con monto excesivo
def test_actualizar_movimiento_monto_excesivo():
    # Primero, creamos un movimiento válido
    movimiento_data = {
        "monto": 1000,
        "tipo": "ingreso",
        "concepto": "Prueba actualización monto alto",
    }
    response_create = client.post("/movimientos/", json=movimiento_data)
    assert response_create.status_code == 200
    movimiento_creado = response_create.json()
    movimiento_id = movimiento_creado["id"]

    # Ahora, intentamos actualizarlo con un monto excesivo
    movimiento_update_data = {
        "monto": 600000,  # Monto excesivo
        "tipo": "egreso",
        "concepto": "Actualización monto alto",
    }
    response_update = client.put(
        f"/movimientos/{movimiento_id}", json=movimiento_update_data
    )
    assert response_update.status_code == 400  # Esperamos un error 400
    assert response_update.json() == {"detail": "Monto excede el límite de seguridad."}
    # Limpieza: Eliminar el movimiento creado
    client.delete(f"/movimientos/{movimiento_id}")


# Test 8: Verificar creación y actualización de un movimiento
def test_crear_y_actualizar_movimiento():
    movimiento_data = {
        "monto": 1500,
        "tipo": "ingreso",
        "concepto": "Prueba creación y actualización",
    }
    # Crear el movimiento
    response_create = client.post("/movimientos/", json=movimiento_data)
    assert response_create.status_code == 200
    movimiento_creado = response_create.json()
    movimiento_id = movimiento_creado["id"]

    # Actualizar el movimiento
    movimiento_update_data = {
        "monto": 2500,
        "tipo": "ingreso",
        "concepto": "Actualización exitosa",
    }
    response_update = client.put(
        f"/movimientos/{movimiento_id}", json=movimiento_update_data
    )
    assert response_update.status_code == 200
    movimiento_actualizado = response_update.json()
    assert movimiento_actualizado["monto"] == 2500
    assert movimiento_actualizado["concepto"] == "Actualización exitosa"
