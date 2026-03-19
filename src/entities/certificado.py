import uuid
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.database.config import Base


class Certificado(Base):
    __tablename__ = "certificado"

    id_certificado = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    
    id_inscripcion = Column(
        UUID(as_uuid=True), ForeignKey("inscripcion.id_inscripcion"), nullable=False
    )

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
    inscripcion = relationship("Inscripcion", foreign_keys=[id_inscripcion])
