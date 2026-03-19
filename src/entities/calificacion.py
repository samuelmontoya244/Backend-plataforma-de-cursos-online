import uuid
from sqlalchemy import Column, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.database.config import Base


class Calificacion(Base):
    __tablename__ = "calificacion"

    ID_inscripcion = Column(PG_UUID(as_uuid=True), ForeignKey("inscripcion.ID_inscripcion"), primary_key=True)
    ID_evaluacion = Column(PG_UUID(as_uuid=True), ForeignKey("evaluacion.id_evaluacion"), primary_key=True)

    Nota = Column(Float, nullable=False)
    Fecha_registro = Column(DateTime(timezone=True), server_default=func.now())

    # trazabilidad
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())
    id_usuario_creacion = Column(PG_UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False)
    id_usuario_edita = Column(PG_UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True)

    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita])

    # relaciones
    inscripcion = relationship("Inscripcion", foreign_keys=[ID_inscripcion])
    evaluacion = relationship("Evaluacion", foreign_keys=[ID_evaluacion])
