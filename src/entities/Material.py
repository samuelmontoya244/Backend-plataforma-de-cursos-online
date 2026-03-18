import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base


class Material(Base):
    """Modelo de material"""

    __tablename__ = "material"

    id_material = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        
    )
    id_leccion = Column(
        UUID(as_uuid=True), ForeignKey("leccion.id_leccion"), nullable=False
    )

    titulo_material = Column[str](
        String(20),
        nullable=False,
    )
    tipo_material = Column[str](String(20), nullable=True)
    URL_archivo = Column[str](String(255), nullable=True)

    id_leccion = Column(
        UUID(as_uuid=True), ForeignKey("leccion.id_leccion"), nullable=False
    )

    leccion = relationship("Leccion", foreign_keys=[id_leccion])
