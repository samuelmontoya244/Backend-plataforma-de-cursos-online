import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func

from src.database.config import Base


class Calificacion(Base):

    __tablename__ = "calificacion"

    id_inscripcion = Column(PG_UUID(as_uuid=True), primary_key=True)
    id_evaluacion = Column(PG_UUID(as_uuid=True), primary_key=True)
    nota = Column(Float, nullable=False)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())


class CalificacionBase(BaseModel):

    nota: float = Field(..., ge=0, le=5)


class CalificacionCreate(CalificacionBase):

    id_inscripcion: UUID
    id_evaluacion: UUID


class CalificacionUpdate(BaseModel):

    nota: Optional[float] = Field(None, ge=0, le=5)


class CalificacionResponse(CalificacionBase):

    id_inscripcion: UUID
    id_evaluacion: UUID
    fecha_registro: datetime

    class Config:
        from_attributes = True
