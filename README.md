**API BIBLIOTECA**

**PARTE 1: DESPLIEGUE DE API EN WINDOWS Y LINUX**

**Despliegue de API en Windows**

Primero  descargamos del repositorio de GitHub , instalamos la versión de python 3.12, instalamos postgresql y  posterior a esto vamos a realizar los siguientes pasos:

**1.Instalamos las librerías necesarias para el funcionamiento de la api.**

Ejecutamos el siguiente comando:

```bash

pip install -r requirements.txt

```


**2.Realizar la configuración de pgadmin.**

- Entramos a pgadmin con la url http:localhost:5050.

- ingresamos usuario usuario y contraseña que definimos en la instalación de postgresql.

- creamos una conexión con el puerto y demás datos definidos en la configuración de instalación del postgresql.

- Una vez la conexión se crea con exito , creamos la base de datos db_biblioteca.


**3. Correr la API.**

Ejecutamos en bash:

```bash

uvicorn app.main:app --reload

```

Una vez la api se levanta crea la tabla "books" en  la base de datos.

**4. Probamos los endpoints en swagger.**

Ingresamos a la url de swagger y probamos los endpoints.


Swagger:**http://127.0.0.1:8000/docs**



**5. Realizar Test.**


Ejecutaamos en bash el siguiente comando:

```bash
pytest -q

```



**DESPLIEGUE DE API DOCKERIZADA EN LINUX**


 Primero escomprimimos la carpeta de la api con unzip o la descargamos del repositorio de GitHub.
 
 Segundo agregamos la siguiente linea al archivo requirements.txt:

 ```bash
 #debajo de las demás librerías ya definidas
 gunicorn>=21.2


```

 Posterior a eso ejecutaremos los siguientes pasos:

**1. Modificar el archivo database.py**

Entrar al archivo database.py y modificar esta linea:

```bash
DATABASE_URL = "postgresql+psycopg2://postgres:12345@localhost:5432/db_biblioteca"
```


"por esta:"

```bash
DATABASE_URL = "postgresql+psycopg2://postgres:12345@pg:5432/db_biblioteca"
```


Esto se hace para que el contenedor de postgres se comunique correctamente ya que también estará dockerizado.

**2. Crear red docker.**

Ejecutamos en la terminal el siguiente comando:

```bash
docker network create books-net || true
```

**3. crear contenedor de postgresql.**
 Ejecutamos en la terminal  el siguiente comando:

 ```bash

 docker run -d --name pg \
  --network books-net \
  -e POSTGRES_DB=db_biblioteca \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=12345 \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  --restart unless-stopped \
  postgres:16

```

**4. crear contenedor de pgadmin**

Ejecutamos el siguiente comando para crear el contenedor de pgadmin:

```bash
docker run -d --name pgadmin \
  --network books-net \
  -e PGADMIN_DEFAULT_EMAIL=admin@admin.com \
  -e PGADMIN_DEFAULT_PASSWORD=admin123 \
  -p 5050:80 \
  --restart unless-stopped \
  dpage/pgadmin4

```

**5. Crear la conexión  en pgadmin**

- Con los parámetros establecidos al crear el contenedor de postgres se crea la conexión y la base de datos por defecto "postgres".

- Luego creamos la base de datos "db_biblioteca".

**Nota:** hacer esto antes de hacer el build del dockerfile.


**4. construir la imagen de la API**

Ejecutamos el siguiente comando para crear la imagen de la api y ejecutar todo el archivo dockerfile.

```bash
docker build -t biblioteca-api:latest .

```

**5. Crear contenedor de la API**

Creamos el contenedor de la API con el siguiente comando:

```bash

docker run -d --name biblioteca_api \
  --network books-net \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql+psycopg2://postgres:12345@pg:5432/db_biblioteca \
  --restart unless-stopped \
  biblioteca-api:latest

```

**6.verificar que todo los contenedores funcionan.**

Ejecutamos el siguiente comando para revisar que los contenedores estén activos y en los puertos correspondientes:

```bash

docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"


```



**7.Probar la API**

Ejecutamos el siguiente comando para saber si la API está funcionando correctamente:

```bash

curl -i http://127.0.0.1:8000/docs

```


**8. Ejecutar  la api en la web**

Ingresar a **http://127.0.0.1:8000/docs** y probar los endpoints.


**PARTE 2: DOCUMENTACIÓN COMPLEMENTARIA DE LA API**

Dejo aquí una explicación general del proyecto, ya que no alcancé a comentar el código directamente.

- La API fue desarrollada con FastAPI, SQLAlchemy y PostgreSQL, y está pensada para manejar el registro y consulta de libros en una base de datos.

- El archivo main.py es el punto de entrada. Ahí se inicializa la aplicación y se crean las tablas automáticamente cuando se levanta el servidor.

- En database.py está la configuración de la conexión con la base de datos y la sesión que usa SQLAlchemy para trabajar.

- El modelo Book está en models.py, que define la estructura de la tabla books (con campos como título, autor, año e ISBN).

- En schemas.py están los modelos de validación con Pydantic, que se usan para revisar los datos que llegan a la API antes de guardarlos o devolverlos.

- Toda la lógica de las operaciones con la base (crear, leer, actualizar, eliminar, filtrar, buscar) está en crud.py.

- Las rutas y endpoints están organizadas en routers/books.py, donde se definen las funciones que responden a cada petición: crear libros, listarlos, filtrarlos, buscarlos o eliminarlos.
También se añadió paginación usando los parámetros skip y limit, para limitar la cantidad de registros que devuelve la API.

- Las pruebas están en la carpeta tests/, hechas con pytest, y usan una base de datos temporal en memoria, así no afecta los datos reales.

- La documentación se genera automáticamente con Swagger y Redoc, y se puede consultar desde el navegador cuando la API está en ejecución.


**Muchas gracias por la oportunidad de presentar esta prueba técnica.**