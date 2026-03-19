import uuid
from sqlalchemy import Column, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func

from src.database.config import Base


class Calificacion(Base):
    """Modelo de calificación (Inscripción-Evaluación)"""

    __tablename__ = "calificacion"

    id_inscripcion = Column(
        PG_UUID(as_uuid=True),
        ForeignKey("inscripcion.id_inscripcion"),
        primary_key=True,
    )
    id_evaluacion = Column(
        PG_UUID(as_uuid=True), ForeignKey("evaluacion.id_evaluacion"), primary_key=True
    )

    nota = Column(Float, nullable=False)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())

    id_usuario_creacion = Column(
        PG_UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )
    id_usuario_edita = Column(
        PG_UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )
