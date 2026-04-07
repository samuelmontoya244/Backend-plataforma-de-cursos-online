from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class CursoCreate(BaseModel):
    id_categoria: UUID
    nombre_curso: str
    duracion_horas: int
    estado_curso: str
    descripcion_curso: str | None = None


class CursoUpdate(BaseModel):
    id_categoria: Optional[UUID] = None
    nombre_curso: Optional[str] = None
    duracion_horas: Optional[int] = None
    estado_curso: Optional[str] = None
    descripcion_curso: Optional[str] = None

class CursoResponse(BaseModel):
    id_curso: UUID
    id_categoria: UUID
    nombre_curso: str
    duracion_horas: int
    estado_curso: str
    descripcion_curso: str | None = None
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True