from main import app


# TEST 1: Verificar que la ruta de inicio responde
def test_read_main(client):
    response = client.get("/")  # Simulamos entrar a "/"
    assert response.status_code == 200  # Esperamos código 200 (OK)
    assert response.json() == {"status": "Online", "version": "Billetera Local 2.0 (Refactorizada)"}


# TEST 2: Verificar la estructura del saldo
def test_read_saldo(client):
    response = client.get("/movimientos/saldo")
    assert response.status_code == 200
    data = response.json()

    # Validamos que la respuesta tenga las llaves correctas
    assert "saldo_actual" in data
    assert "moneda" in data
    assert data["moneda"] == "ARS"


# TEST 3: Verificar creación de un movimiento con monto excesivo
def test_crear_movimiento_monto_excesivo(client, categoria_test):
    categoria_id = categoria_test["id"]
    movimiento_data = {
        "monto": 600000,  # Monto excesivo
        "tipo": "egreso",
        "concepto": "Prueba monto alto",
        "categoria_id": categoria_id
    }
    response = client.post("/movimientos/", json=movimiento_data)
    assert response.status_code == 400  # Esperamos un error 400
    assert response.json() == {"detail": "Monto excede el límite de seguridad."}


# TEST 4: Verificar eliminación de un movimiento inexistente
def test_eliminar_movimiento_inexistente(client):
    response = client.delete("/movimientos/9999")  # ID que no existe
    assert response.status_code == 404  # Esperamos un error 404
    assert response.json() == {"detail": "Movimiento no encontrado."}


# TEST 5: Verificar creación y eliminación de un movimiento
def test_crear_y_eliminar_movimiento(client, categoria_test):
    categoria_id = categoria_test["id"]
    movimiento_data = {
        "monto": 1000,
        "tipo": "ingreso",
        "concepto": "Prueba creación y eliminación",
        "categoria_id": categoria_id
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
def test_actualizar_movimiento_inexistente(client, categoria_test):
    categoria_id = categoria_test["id"]
    movimiento_data = {
        "monto": 2000,
        "tipo": "egreso",
        "concepto": "Prueba actualización inexistente",
        "categoria_id": categoria_id
    }
    response = client.put("/movimientos/9999", json=movimiento_data)  # ID que no existe
    assert response.status_code == 404  # Esperamos un error 404
    assert response.json() == {"detail": "Movimiento no encontrado."}


# TEST 7: Verificar actualización de un movimiento con monto excesivo
def test_actualizar_movimiento_monto_excesivo(client, categoria_test):
    categoria_id = categoria_test["id"]
    # Primero, creamos un movimiento válido
    movimiento_data = {
        "monto": 1000,
        "tipo": "ingreso",
        "concepto": "Prueba actualización monto alto",
        "categoria_id": categoria_id
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
        "categoria_id": categoria_id
    }
    response_update = client.put(
        f"/movimientos/{movimiento_id}", json=movimiento_update_data
    )
    assert response_update.status_code == 400  # Esperamos un error 400
    assert response_update.json() == {"detail": "Monto excede el límite de seguridad."}
    # Limpieza: Eliminar el movimiento creado
    client.delete(f"/movimientos/{movimiento_id}")


# Test 8: Verificar creación y actualización de un movimiento
def test_crear_y_actualizar_movimiento(client, categoria_test):
    categoria_id = categoria_test["id"]
    movimiento_data = {
        "monto": 1500,
        "tipo": "ingreso",
        "concepto": "Prueba creación y actualización",
        "categoria_id": categoria_id
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
        "categoria_id": categoria_id
    }
    response_update = client.put(
        f"/movimientos/{movimiento_id}", json=movimiento_update_data
    )
    assert response_update.status_code == 200
    movimiento_actualizado = response_update.json()
    assert movimiento_actualizado["monto"] == 2500
    assert movimiento_actualizado["concepto"] == "Actualización exitosa"
#Test 9: Crear movimiento con categoria inexistente
def test_crear_movimiento_categoria_inexistente(client):
    movimiento_data = {
        "monto": 1000,
        "tipo": "ingreso",
        "concepto": "Prueba categoria inexistente",
        "categoria_id": 9999  # Categoria que no existe
    }
    response = client.post("/movimientos/", json=movimiento_data)
    assert response.status_code == 404  # Esperamos un error 404
    assert response.json() == {"detail": "Categoría no encontrada."}
    # Limpieza: Eliminar el movimiento creado
#Test 10: Crear categoria y leer categorias
def test_crear_y_leer_categorias(client):
    categoria_data = {
        "nombre": "Prueba Categoria"
    }
    # Crear la categoria
    response_create = client.post("/categorias/", json=categoria_data)
    assert response_create.status_code == 200
    categoria_creada = response_create.json()
    categoria_id = categoria_creada["id"]

    # Leer las categorias
    response_read = client.get("/categorias/")
    assert response_read.status_code == 200
    categorias = response_read.json()
    assert any(cat["id"] == categoria_id for cat in categorias)
#Test 11: Crear movimiento con categoria existente
def test_crear_movimiento_categoria_existente(client):
    categoria_data = {
        "nombre": "Categoria para Movimiento"
    }
    # Crear la categoria
    response_create_cat = client.post("/categorias/", json=categoria_data)
    assert response_create_cat.status_code == 200
    categoria_creada = response_create_cat.json()
    categoria_id = categoria_creada["id"]

    movimiento_data = {
        "monto": 2000,
        "tipo": "ingreso",
        "concepto": "Prueba categoria existente",
        "categoria_id": categoria_id
    }
    # Crear el movimiento
    response_create_mov = client.post("/movimientos/", json=movimiento_data)
    assert response_create_mov.status_code == 200
    movimiento_creado = response_create_mov.json()
    assert movimiento_creado["categoria_id"] == categoria_id

#Test 12: Crear usuario y verificar hash de contraseña
def test_crear_usuario_y_verificar_hash(client):
    usuario_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "securepassword123"
    }
    response = client.post("/auth/register", json=usuario_data)
    assert response.status_code == 200
    usuario_creado = response.json()
    assert usuario_creado["username"] == "testuser"
    assert usuario_creado["email"] == "testuser@example.com"
    assert "hashed_password" not in usuario_creado  # No debe devolver la contraseña hasheada