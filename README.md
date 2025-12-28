# Personal Finance API 💰

A robust, high-performance **RESTful API** built with **Python** and **FastAPI** to manage personal finances. This project demonstrates backend engineering best practices, including **Data Validation**, **Relational Database Design**, **Dependency Injection**, and **Automated Integration Testing**.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Passing-4b8bbe?style=for-the-badge&logo=pytest&logoColor=white)
![SQLModel](https://img.shields.io/badge/ORM-SQLModel-black?style=for-the-badge)

## 📖 Project Overview

This backend application solves the problem of tracking financial movements (incomes/expenses) with temporal context and categorization. It provides endpoints for creating, reading, updating, and deleting (CRUD) transactions, with advanced capabilities for **filtering**, **sorting**, and **relationship management**.

The core philosophy of this project is **Reliability** and **Maintainability**, achieved through strict type checking, separation of concerns, and a comprehensive test suite.

## 🏗️ Technical Architecture & Design Patterns

The project follows a **Layered Architecture** to ensure separation of concerns (SoC), adhering to **SOLID principles**:

* **Models Layer (`models.py`):** Defines the database schema using **SQLModel (SQLAlchemy)**. Handles persistence and table relationships (One-to-Many between Categories and Movements).
* **Schemas Layer (`schemas.py`):** Handles Data Transfer Objects (DTOs) using **Pydantic V2**. This layer acts as a "security guard," validating input data and serializing output data (excluding sensitive internal fields).
* **Controller Layer (`main.py`):** Manages HTTP requests and business logic. It utilizes **Dependency Injection** to manage database sessions securely.
* **Configuration (`settings.py`):** Decouples configuration from code using environment variables (12-Factor App methodology).

### Key Features
* **✅ Full CRUD Operations:** Create, Read, Update, and Delete for Movements and Categories.
* **🔌 Relational Integrity:** Enforces Foreign Keys to ensure data consistency between Transactions and Categories.
* **🔍 Advanced Filtering & Sorting:** * Dynamic query parameters to filter by date range (`fecha_desde`, `fecha_hasta`), category, or type.
    * Safe dynamic sorting via `order_by` (protected against injection).
* **🛡️ Robust Error Handling:** Custom HTTP exceptions for business rules (e.g., transaction limits, non-existent foreign keys).
* **♻️ Data Seeding:** Automated script (`seed.py`) to populate the database with realistic mock data for development and staging.

## 🛠️ Tech Stack

* **Language:** Python 3.11+
* **Framework:** FastAPI (High performance, async support)
* **ORM:** SQLModel (Combines SQLAlchemy and Pydantic)
* **Validation:** Pydantic V2
* **Database:** SQLite (Easily scalable to PostgreSQL)
* **Testing:** Pytest & HTTPX

## 🧪 Testing Strategy

Quality assurance is a priority. The project includes a suite of **Integration Tests** that cover happy paths and edge cases.

* **Isolation:** Tests run on an **in-memory SQLite database** using `StaticPool`. This ensures that tests never corrupt the production/development database and are concurrency-safe.
* **Fixtures:** Utilizes `pytest` fixtures in `conftest.py` for setup/teardown automation and dependency overrides.
* **Coverage:** Validates HTTP status codes, JSON response structures, database integrity, and complex scenarios like "Update with Partial Data".

## 🚀 Getting Started

### Prerequisites
* Python 3.10 or higher
* Git

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/PROJECT_NAME.git](https://github.com/YOUR_USERNAME/PROJECT_NAME.git)
    cd PROJECT_NAME
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```

5.  **Access Documentation:**
    * Swagger UI: `http://127.0.0.1:8000/docs`
    * ReDoc: `http://127.0.0.1:8000/redoc`

### Data Seeding (Optional)
Populate the database with dummy data (Categories and Movements) for testing purposes:
```bash
python seed.py
