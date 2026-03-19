import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base

class Curso(Base):
    """Modelo de curso"""

    __tablename__ = "curso"

    id_curso = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_categoria = Column(
        UUID(as_uuid=True), ForeignKey("categoria.id_categoria"), nullable=False
    )

    nombre_curso = Column(String(100), nullable=False)
    descripcion_curso = Column(Text, nullable=True)
    duracion_horas = Column(Integer, nullable=False)
    estado_curso = Column(String(50), nullable=False)
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
    categoria = relationship("Categoria", foreign_keys=[id_categoria])
