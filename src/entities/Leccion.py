import uuid

from sqlalchemy import Column, ForeignKey, String, Text, int
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base


class Leccion(Base):
    """Modelo de lección"""

    __tablename__ = "leccion"

    id_leccion = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        unique=True,
    )
    id_curso = Column(UUID(as_uuid=True), ForeignKey("curso.id_curso"), nullable=False)

    titulo_leccion = Column[str](
        String(20),
        nullable=False,
    )
    descripcion_leccion = Column[str](Text, nullable=True)
    orden = Column[int](int, nullable=False, unique=True)
    duracion_horas = Column[int](int, nullable=False)

    id_curso = Column(UUID(as_uuid=True), ForeignKey("curso.id_curso"), nullable=False)

    curso = relationship("Curso", foreign_keys=[id_curso])
