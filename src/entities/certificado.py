"""
Entidad Certificado: documento emitido tras completar un curso.
"""

import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func

from src.database.config import Base


class Certificado(Base):

    __tablename__ = "certificado"

    id_certificado = Column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    fecha_expedicion = Column(DateTime(timezone=True), server_default=func.now())
    id_inscripcion = Column(PG_UUID(as_uuid=True), nullable=False)


class CertificadoBase(BaseModel):

    id_inscripcion: UUID


class CertificadoCreate(CertificadoBase):

    pass


class CertificadoUpdate(BaseModel):

    fecha_expedicion: Optional[datetime] = None


class CertificadoResponse(CertificadoBase):

    id_certificado: UUID
    fecha_expedicion: datetime

    class Config:
        from_attributes = True
