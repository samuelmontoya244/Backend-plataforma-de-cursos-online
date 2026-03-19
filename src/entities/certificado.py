import uuid
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func

from src.database.config import Base


class Certificado(Base):
    """Modelo de certificado"""

    __tablename__ = "certificado"

    id_certificado = Column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    fecha_expedicion = Column(DateTime(timezone=True), server_default=func.now())
    id_inscripcion = Column(
        PG_UUID(as_uuid=True), ForeignKey("inscripcion.id_inscripcion"), nullable=False
    )

    id_usuario_creacion = Column(
        PG_UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )
    id_usuario_edita = Column(
        PG_UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )
