import uuid

from sqlalchemy import Column, ForeignKey, String, Float, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base


class Evaluacion(Base):
    """Modelo de evaluación"""

    __tablename__ = "evaluacion"

    id_evaluacion = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    
    id_leccion = Column(
        UUID(as_uuid=True), ForeignKey("leccion.id_leccion"), nullable=False, unique=True
    )


    nombre_evaluacion = Column(String(20),nullable=False)
    porcentaje = Column(Float, nullable=False)
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
    leccion = relationship("Leccion", foreign_keys=[id_leccion])