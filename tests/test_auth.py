from main import app
def test_crear_usuario_y_verificar_hash(client):
    usuario_data = {
        "username": "usuario_nuevo", 
        "email": "test2@test.com",
        "password": "securepassword123"
    }
    response = client.post("/auth/register", json=usuario_data)
    assert response.status_code == 200
    usuario_creado = response.json()
    assert usuario_creado["username"] == "usuario_nuevo"
    assert usuario_creado["email"] == "test2@test.com"
    assert "hashed_password" not in usuario_creado  # No debe devolver la contraseña hasheada