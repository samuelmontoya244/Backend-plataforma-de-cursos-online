from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class CursoCreate(BaseModel):
    id_categoria: UUID
    nombre_curso: str
    duracion_horas: int
    estado_curso: str
    id_usuario_creacion: UUID
    descripcion_curso: Optional[str] = None


class CursoUpdate(BaseModel):
    id_categoria: Optional[UUID] = None
    nombre_curso: Optional[str] = None
    duracion_horas: Optional[int] = None
    estado_curso: Optional[str] = None
    id_usuario_creacion: Optional[UUID] = None
    descripcion_curso: Optional[str] = None


class CursoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_curso: UUID
    id_categoria: UUID
    nombre_curso: str
    duracion_horas: int
    estado_curso: str
    id_usuario_creacion: UUID
    descripcion_curso: str | None = None

class CursoResponse(BaseModel):
    id_curso: UUID
    id_categoria: UUID
    nombre_curso: str
    duracion_horas: int
    estado_curso: str
    id_usuario_creacion: UUID
    descripcion_curso: str
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True

# Modelos de respuesta para la API
class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool = True
    datos: Optional[dict] = None