# app/tests/conftest.py
import os, sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

# Asegura que la raíz del proyecto esté en sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.database import Base, get_db
from app.main import app
# 👇 IMPORTANTE: registrar modelos en Base.metadata
from app import models  # NO borrar

# 1) Engine de prueba: SQLite en memoria + StaticPool (misma conexión)
TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"
engine_test = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # 👈 clave para que no se pierdan tablas entre conexiones
)

# 2) Session maker de prueba
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

# 3) Crear/limpiar tablas alrededor de cada test
@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine_test)
    try:
        yield
    finally:
        Base.metadata.drop_all(bind=engine_test)

# 4) Override de la dependencia get_db para usar la sesión de prueba
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# 5) Cliente de prueba
@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c
