"""
Aplicacion FastAPI, Ejecutar con:
    uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
"""

from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.security import HTTPBearer
from src.utils.jwt_utils import decode_jwt

from fastapi import FastAPI

from src.database.config import create_tables
from src.endpoints import (
    usuario,
    inscripcion,
    curso,
    leccion,
    material,
    pago,
    certificado,
    evaluacion,
    categoria,
    calificacion,
)

security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Crea las tablas al iniciar la aplicación."""
    create_tables()
    yield


app = FastAPI(
    title="Plataforma de Cursos Online - Backend",
    description="API para gestionar usuarios, cursos, inscripciones y más.",
    version="1.0.0",
    lifespan=lifespan,
)

# ✅ CORREGIDO: CORS va primero, antes de cualquier otro middleware
# Si va después, las preflight OPTIONS son interceptadas por el middleware
# de auth antes de que CORS pueda responderlas, bloqueando todas las peticiones
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
        "https://plataforma-de-cursos-onl-507ce.web.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ CORREGIDO: el middleware de auth ignora las preflight OPTIONS
# para que CORS pueda manejarlas correctamente
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    # Dejar pasar las preflight requests sin tocarlas
    if request.method == "OPTIONS":
        return await call_next(request)

    auth_header = request.headers.get("Authorization")

    if auth_header and auth_header.startswith("Bearer "):
        try:
            token = auth_header.replace("Bearer ", "")
            payload = decode_jwt(token)
            request.state.user = payload
        except Exception:
            request.state.user = None
    else:
        request.state.user = None

    response = await call_next(request)
    return response

app.include_router(usuario.router)
app.include_router(inscripcion.router)
app.include_router(curso.router)
app.include_router(leccion.router)
app.include_router(material.router)
app.include_router(pago.router)
app.include_router(certificado.router)
app.include_router(evaluacion.router)
app.include_router(categoria.router)
app.include_router(calificacion.router)


@app.get("/")
def inicio():
    return {
        "message": "Bienvenido a la API de la Plataforma de Cursos Online",
        "data": {"mensaje": "API Plataforma de Cursos Online", "docs": "/docs"},
    }