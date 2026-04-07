""""
Aplicacion FastAPI, Ejecutar con: 
    uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.config import create_tables
from src.endpoints import (
    usuario,
<<<<<<< Updated upstream
    leccion,
    material,
    pago
=======
    #inscripcion,
    #curso
>>>>>>> Stashed changes
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Crea las tablas al iniciar la aplicación."""
    create_tables()
    yield

app = FastAPI(
    title="Plataforma de Cursos Online - Backend",
    description="API para gestionar usuarios, cursos, inscripciones y más.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(usuario.router)
<<<<<<< Updated upstream
#app.include_router(leccion.router)
#app.include_router(material.router)
#app.include_router(pago.router)
=======
#app.include_router(inscripcion.router)
#app.include_router(curso.router)

>>>>>>> Stashed changes

@app.get("/")
def inicio():
    return {
        "message": "Bienvenido a la API de la Plataforma de Cursos Online",
        "data": {"mensaje": "API Plataforma de Cursos Online", "docs": "/docs"},
    }
