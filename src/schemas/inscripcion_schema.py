from datetime import datetime
from typing import Optional
from uuid import UUID
from src.entities.inscripcion import EstadoInscripcion

from pydantic import BaseModel, ConfigDict

class InscripcionCreate(BaseModel):
    id_curso: UUID
    id_usuario_inscrito: UUID
    estado_inscripcion: str = None


class InscripcionUpdate(BaseModel):
    id_curso: Optional[UUID] = None
    id_usuario_inscrito: Optional[UUID] = None
    estado_inscripcion: Optional[str] = None

class InscripcionResponse(BaseModel):
    id_inscripcion: UUID
    id_curso: UUID
    id_usuario_inscrito: UUID
    estado_inscripcion: str = None
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True