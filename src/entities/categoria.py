import uuid
from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func

from src.database.config import Base


class Categoria(Base):
    """Modelo de categoría"""

    __tablename__ = "categoria"

    id_categoria = Column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    nombre_categoria = Column(String(150), nullable=False, unique=True)
    descripcion = Column(String(255), nullable=True)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    id_usuario_creacion = Column(
        PG_UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )
    id_usuario_edita = Column(
        PG_UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )
