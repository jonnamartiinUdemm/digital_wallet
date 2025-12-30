from main import app
#Crear categoria y leer categorias
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