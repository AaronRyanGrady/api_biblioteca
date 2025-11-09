
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .database import engine
from . import models


from .routers.books import router as books_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    
    models.Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas en la base de datos.")
    yield
    
    print("👋 Aplicación finalizada.")

app = FastAPI(
    title="Biblioteca API",
    version="0.1.0",
    description="API REST para gestionar una pequeña biblioteca",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/", tags=["status"])
def read_root():
    return {"status": "ok", "message": "Biblioteca API - Etapa 1"}

@app.get("/health", tags=["status"])
def health():
    return {"status": "healthy"}

# Registrar rutas de libros
app.include_router(books_router)