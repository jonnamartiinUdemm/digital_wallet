# 💰 Billetera Virtual - Backend API

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![Coverage](https://img.shields.io/badge/Tests-Passing-brightgreen)

API RESTful para la gestión de finanzas personales. Permite a los usuarios registrar ingresos y egresos, categorizarlos, consultar saldos y filtrar movimientos históricos. El sistema cuenta con autenticación segura y está desplegado en la nube.

## 🚀 Demo en Vivo

Puedes probar la documentación interactiva (Swagger UI) aquí:
👉 **[https://jnnmnn-billetera-api.onrender.com/docs](https://jnnmnn-billetera-api.onrender.com/docs)**

*(Nota: Al estar en un plan gratuito de Render, el servidor puede tardar unos segundos en "despertar" si no se ha usado recientemente).*

## ✨ Características Principales

* **Autenticación Segura:** Registro y Login de usuarios mediante **JWT (JSON Web Tokens)** y hashing de contraseñas con **Bcrypt**.
* **Gestión de Movimientos:** CRUD completo (Crear, Leer, Actualizar, Borrar).
* **Filtros Avanzados:** Consultar movimientos por tipo (ingreso/egreso), categoría o rango de fechas.
* **Categorías:** Gestión dinámica de categorías para organizar los gastos.
* **Seguridad de Negocio:** Validaciones de límites de transferencia y saldos.
* **Testing:** Suite de pruebas automatizadas con **Pytest** (cobertura de Auth, Movimientos y Categorías).
* **Containerización:** Listo para desplegar con **Docker**.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.11
* **Framework:** FastAPI
* **ORM:** SQLModel (SQLAlchemy + Pydantic)
* **Base de Datos:** SQLite (Desarrollo/Demo)
* **Seguridad:** Passlib (Bcrypt), Python-Jose (JWT)
* **Testing:** Pytest, TestClient
* **Infraestructura:** Docker, Render

## ⚙️ Instalación Local

Sigue estos pasos para correr el proyecto en tu máquina:

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/TU_USUARIO/billetera-backend.git](https://github.com/TU_USUARIO/billetera-backend.git)
    cd billetera-backend
    ```

2.  **Crear entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Variables de Entorno:**
    Crea un archivo `.env` en la raíz y agrega:
    ```env
    SECRET_KEY="tu_clave_secreta_super_larga"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    LIMITE_TRANSFERENCIA=500000
    NOMBRE_APP="Billetera Local"
    ```

5.  **Ejecutar el servidor:**
    ```bash
    uvicorn main:app --reload
    ```
    La API estará disponible en `http://localhost:8000/docs`.

## 🐳 Ejecución con Docker

Si tienes Docker instalado, no necesitas configurar Python ni entornos virtuales:

1.  **Construir la imagen:**
    ```bash
    docker build -t billetera-backend .
    ```

2.  **Correr el contenedor:**
    ```bash
    docker run -d -p 8000:8000 --name mi-api billetera-backend
    ```

## 🧪 Testing

El proyecto cuenta con pruebas modulares. Para ejecutarlas:

```bash
pytest