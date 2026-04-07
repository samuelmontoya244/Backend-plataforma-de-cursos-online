from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class CategoriaCreate(BaseModel):
    nombre_categoria: str


class CategoriaUpdate(BaseModel):
    nombre_categoria: Optional[str] = None


class CategoriaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_categoria: UUID
    nombre_categoria: str

class CategoriaResponse(BaseModel):
    id_categoria: UUID
    nombre_categoria: str
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True

# Modelos de respuesta para la API
class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool = True
    datos: Optional[dict] = None