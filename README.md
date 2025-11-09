# Biblioteca API 📚

API REST con FastAPI + SQLAlchemy + PostgreSQL para gestionar libros.

## Requisitos
- Python 3.12+
- PostgreSQL 16+ (DB: `db_biblioteca`)
- (Opcional) Docker

## Instalación
```bash
python -m venv .venv && .venv\Scripts\activate  # (Windows)
pip install -r requirements.txt


## Configuración de conexión a bd

postgresql+psycopg2://postgres:12345@localhost:5432/db_biblioteca



#ejecutar uvicorn

uvicorn app.main:app --reload


##urls de swager

Swagger: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

Health: http://127.0.0.1:8000/health

##Endpoints

POST /libros (acepta lista o un libro según tu implementación)

GET /libros?author=&year=&skip=0&limit=10

GET /libros/search?q=texto

GET /libros/{id}

PUT /libros/{id}

DELETE /libros/{id}

# Tests 

Ejecutar en bash:

pytest -q
#(Usan SQLite en memoria con StaticPool; no tocan tu Postgres.)


# levantar contenedor

docker compose up --build


DESPLEGAR CONTENEDORES

Paso 1: crear una red para que API ↔ Postgres se vean

docker network create books-net


Paso 2: levantar Postgres (con volumen para persistir datos)

docker run -d --name pg \
  --network books-net \
  -e POSTGRES_DB=db_biblioteca \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=12345 \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  --restart unless-stopped \
  postgres:16

paso 3:crear contenedor de pgadmin

docker run -d --name pgadmin \
  --network books-net \
  -e PGADMIN_DEFAULT_EMAIL=admin@admin.com \
  -e PGADMIN_DEFAULT_PASSWORD=admin123 \
  -p 5050:80 \
  --restart unless-stopped \
  dpage/pgadmin4

Paso 4: abrir pg admin en el navegador

url: http://localhost:5050



Inicia sesión con:

Email: admin@admin.com

Password: admin123


 paso 5


creamos la conexión  con lo que indicamos en la creación de la imagen del contenedor de postgres


paso 6 

creamos la base datos db_biblioteca


paso 7 

verificamos la network que haya quedado bien creada con el siguiente comando:

docker network ls




DESPLIEGUE DE LA API


Paso 1 - descomprimimos la carpeta de la api con unzip o la descargamos del repositorio de GitHub


paso 2 - corremos el dockerfile  de la api

docker build -t biblioteca-api:latest .


paso 3 - creamos el contenedor de la api

docker run -d --name biblioteca_api \
  --network books-net \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql+psycopg2://postgres:12345@pg:5432/db_biblioteca \
  --restart unless-stopped \
  biblioteca-api:latest


paso 4- verificamos un endpoint para ver si la api funciona correctamente

curl http://localhost:8000/health