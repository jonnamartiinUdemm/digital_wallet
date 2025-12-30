# 💰 Billetera Virtual - Cloud Architecture

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791)
![Azure](https://img.shields.io/badge/Azure-Cloud-0078D4)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)
![CI/CD](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-2088FF)

Backend robusto para gestión financiera personal, diseñado con una arquitectura moderna de microservicios y desplegado en la nube con integración continua.

## 🚀 Demo en Vivo

* **API Documentation (Swagger):** [https://jnnmnn-billetera-api.onrender.com/docs](https://jnnmnn-billetera-api.onrender.com/docs)
* **Estado del Deploy:** ![CI/CD Billetera](https://github.com/jonnamartiinUdemm/billetera-backend/actions/workflows/ci.yml/badge.svg)

*(Nota: El servidor está alojado en Render (Free Tier) y la Base de Datos en Azure (Brasil). Puede tardar unos segundos en "despertar" la primera vez).*

## 🏛️ Arquitectura del Sistema

El proyecto sigue una arquitectura distribuida híbrida:

1.  **API (Compute):** Contenedor Docker alojado en **Render**.
2.  **Base de Datos (Storage):** PostgreSQL gestionado en **Azure Database (Flexible Server)**.
3.  **CI/CD Pipeline:** Automatización completa con **GitHub Actions**.

```mermaid
graph LR
    User((👤 Usuario)) --> |HTTPS| Render[☁️ Render (FastAPI Container)]
    Render --> |Secure Connection| Azure[🗄️ Azure PostgreSQL]
    
    subgraph GitHub_Actions [🤖 CI/CD Pipeline]
        Code[📝 Push Code] --> Test[🧪 Pytest]
        Test --> |Success| Deploy[🚀 Auto-Deploy to Render]
    end
```

## ✨ Características Técnicas

* **Base de Datos Híbrida:** Soporte dinámico para **SQLite** (Testing/Dev) y **PostgreSQL** (Producción).
* **Containerización:** Orquestación de servicios (API + DB) mediante **Docker Compose**.
* **Resiliencia:** Lógica de "Retry Pattern" para conexiones a base de datos.
* **Seguridad:** Autenticación JWT (HS256) y Hashing de contraseñas (Bcrypt).
* **Automatización:**
    * **CI:** Ejecución automática de tests en cada `git push`.
    * **CD:** Despliegue automático a producción solo si los tests pasan.

## 🛠️ Tecnologías

* **Core:** Python 3.11, FastAPI, SQLModel.
* **Infraestructura:** Docker, Docker Compose.
* **Base de Datos:** PostgreSQL (Producción), SQLite (Tests).
* **DevOps:** GitHub Actions, Render Deploy Hooks.
* **Cloud:** Microsoft Azure for Students.

## ⚙️ Instalación Local (Con Docker)

La forma más profesional de correr el proyecto es usando Docker Compose, que levanta la API y una base de datos PostgreSQL local idéntica a la de producción.

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/TU_USUARIO/billetera-backend.git](https://github.com/TU_USUARIO/billetera-backend.git)
    cd billetera-backend
    ```

2.  **Configurar Variables:**
    Crea un archivo `.env` en la raíz (Docker lo leerá automáticamente):
    ```env
    SECRET_KEY="clave_secreta_local"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    LIMITE_TRANSFERENCIA=500000
    NOMBRE_APP="Billetera Docker"
    # No es necesario definir DATABASE_URL aquí, docker-compose la inyecta sola.
    ```

3.  **Levantar el entorno:**
    ```bash
    docker compose up --build
    ```

4.  **Acceder:**
    * API Swagger: `http://localhost:8000/docs`
    * La base de datos PostgreSQL estará corriendo en el puerto `5432`.

## 🧪 Testing

El proyecto cuenta con una suite de pruebas automatizadas que se ejecutan tanto localmente como en GitHub Actions.

Para correr los tests manualmente (usando una DB temporal en memoria):

```bash
# Si usas entorno virtual de Python
pytest -v
```

## 📂 Estructura del Proyecto

```text
├── .github/workflows # Pipelines de CI/CD
├── routers/          # Endpoints modulares
├── tests/            # Tests unitarios y de integración
├── database.py       # Conexión con lógica de reintentos
├── docker-compose.yml# Orquestación de servicios
├── Dockerfile        # Receta de la imagen
├── main.py           # Entrypoint
├── models.py         # Modelos SQLModel
└── settings.py       # Gestión de configuración
```

## ✒️ Autor

**Jonathan Martin** - *Software Engineer Student*