from main import app
# TEST 1: Verificar que la ruta de inicio responde
def test_read_main(client):
    response = client.get("/")  # Simulamos entrar a "/"
    assert response.status_code == 200  # Esperamos código 200 (OK)
    assert response.json() == {"status": "Online", "version": "Billetera Local 2.0 (Refactorizada)"}

