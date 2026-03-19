import uuid
from enum import Enum

from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base

class EstadoInscripcion(str, Enum):
    ACTIVA = "ACTIVA"
    FINALIZADA = "FINALIZADA"
    CANCELADA = "CANCELADA"
    APROBADA = "APROBADA"
    REPROBADA = "REPROBADA"

class Inscripcion(Base):
    """Modelo de inscripción"""

    __tablename__ = "inscripcion"

    id_inscripcion = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_curso = Column(
        UUID(as_uuid=True), ForeignKey("curso.id_curso"), nullable=False
    )
    id_usuario_inscrito = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )

    estado_inscripcion = Column(String(50), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())
    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )
    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )

    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita])
    curso = relationship("Curso", foreign_keys=[id_curso])
    usuario_inscrito = relationship("Usuario", foreign_keys=[id_usuario_inscrito])
