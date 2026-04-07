from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CertificadoCreate(BaseModel):
    id_inscripcion: UUID
    id_usuario_creacion: UUID


class CertificadoUpdate(BaseModel):
    id_inscripcion: Optional[UUID] = None
    id_usuario_edita: Optional[UUID] = None


class CertificadoResponse(BaseModel):
    id_certificado: UUID
    id_inscripcion: UUID
    id_usuario_creacion: UUID
    id_usuario_edita: Optional[UUID] = None
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True