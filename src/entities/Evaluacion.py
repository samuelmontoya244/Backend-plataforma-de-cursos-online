import uuid

from sqlalchemy import Column, ForeignKey, String, Float, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base


class Evaluacion(Base):
    """Modelo de evaluación"""

    __tablename__ = "evaluacion"

    id_evaluacion = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    
    id_leccion = Column(
        UUID(as_uuid=True), ForeignKey("leccion.id_leccion"), nullable=False
    )


    nombre_evaluacion = Column[str](
        String(20),
        nullable=False,
    )
    porcentaje = Column[float](Float, nullable=True)
    nota_maxima = Column[str](String(10), nullable=True)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    id_leccion = Column(
        UUID(as_uuid=True), ForeignKey("leccion.id_leccion"), nullable=False
    )

    leccion = relationship("Leccion", foreign_keys=[id_leccion])
