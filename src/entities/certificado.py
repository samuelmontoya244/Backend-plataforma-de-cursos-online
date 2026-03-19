import uuid
from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.database.config import Base


class Certificado(Base):
    __tablename__ = "certificado"

    ID_certificado = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    Nombre_certificado = Column(String(150), nullable=False)

    ID_inscripcion = Column(PG_UUID(as_uuid=True), ForeignKey("inscripcion.ID_inscripcion"), nullable=False)

    # trazabilidad
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())
    id_usuario_creacion = Column(PG_UUID(as_uuid=True), ForeignKey("usuario.ID_usuario"), nullable=False)
    id_usuario_edita = Column(PG_UUID(as_uuid=True), ForeignKey("usuario.ID_usuario"), nullable=True)

    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita])

    # relación con Inscripcion
    inscripcion = relationship("Inscripcion", back_populates="certificados")