from main import app
#Verificar la estructura del saldo
def test_read_saldo(client):
    response = client.get("/movimientos/saldo")
    assert response.status_code == 200
    data = response.json()

    # Validamos que la respuesta tenga las llaves correctas
    assert "saldo_actual" in data
    assert "moneda" in data
    assert data["moneda"] == "ARS"


#Verificar creación de un movimiento con monto excesivo
def test_crear_movimiento_monto_excesivo(client, categoria_test):
    categoria_id = categoria_test.id
    movimiento_data = {
        "monto": 600000,  # Monto excesivo
        "tipo": "egreso",
        "concepto": "Prueba monto alto",
        "categoria_id": categoria_id
    }
    response = client.post("/movimientos/", json=movimiento_data)
    assert response.status_code == 400  # Esperamos un error 400
    assert response.json() == {"detail": "Monto excede el límite de seguridad."}


#Verificar eliminación de un movimiento inexistente
def test_eliminar_movimiento_inexistente(client):
    response = client.delete("/movimientos/9999")  # ID que no existe
    assert response.status_code == 404  # Esperamos un error 404
    assert response.json() == {"detail": "Movimiento no encontrado."}


#Verificar creación y eliminación de un movimiento
def test_crear_y_eliminar_movimiento(client, categoria_test):
    categoria_id = categoria_test.id
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


#Verificar actualización de un movimiento inexistente
def test_actualizar_movimiento_inexistente(client, categoria_test):
    categoria_id = categoria_test.id
    movimiento_data = {
        "monto": 2000,
        "tipo": "egreso",
        "concepto": "Prueba actualización inexistente",
        "categoria_id": categoria_id
    }
    response = client.put("/movimientos/9999", json=movimiento_data)  # ID que no existe
    assert response.status_code == 404  # Esperamos un error 404
    assert response.json() == {"detail": "Movimiento no encontrado."}


#Verificar actualización de un movimiento con monto excesivo
def test_actualizar_movimiento_monto_excesivo(client, categoria_test):
    categoria_id = categoria_test.id
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


#Verificar creación y actualización de un movimiento
def test_crear_y_actualizar_movimiento(client, categoria_test):
    categoria_id = categoria_test.id
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
#Crear movimiento con categoria inexistente
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

#Crear movimiento con categoria existente
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

#Traer movimientos de un solo tipo
def test_traer_movimientos_un_tipo(client, categoria_test):
    categoria_id = categoria_test.id
    # Crear movimientos de diferentes tipos
    movimiento_data_egreso = {
        "monto": 1000,
        "tipo": "egreso",
        "concepto": "Prueba egreso",
        "categoria_id": categoria_id
    }
    movimiento_data_ingreso = {
        "monto": 2000,
        "tipo": "ingreso",
        "concepto": "Prueba ingreso",
        "categoria_id": categoria_id
    }
    client.post("/movimientos/", json=movimiento_data_egreso)
    client.post("/movimientos/", json=movimiento_data_ingreso)

    # Traer solo movimientos de tipo 'egreso'
    response = client.get("/movimientos/?tipo=egreso")
    assert response.status_code == 200
    movimientos = response.json()
    for mov in movimientos:
        assert mov["tipo"] == "egreso"

#Crear movimiento con fondos insuficientes
def test_crear_movimiento_fondos_insuficientes(client, categoria_test):
    categoria_id = categoria_test.id
    movimiento_data = {
        "monto": 5000,  # Monto mayor al saldo disponible (0 al inicio)
        "tipo": "egreso",
        "concepto": "Prueba fondos insuficientes",
        "categoria_id": categoria_id
    }
    response = client.post("/movimientos/", json=movimiento_data)
    assert response.status_code == 400  # Esperamos un error 400
    assert response.json() == {"detail": "Fondos insuficientes para este egreso."}