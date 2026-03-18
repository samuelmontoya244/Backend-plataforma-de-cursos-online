import uuid

from sqlalchemy import Column, ForeignKey, String, Float, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base


class Pago(Base):
    """Modelo de pago"""

    __tablename__ = "pago"

    id_pago = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        
    )
    id_usuario = Column(
        UUID(as_uuid=True), ForeignKey("leccion.id_leccion"), nullable=False
    )

    id_curso = Column(
        UUID(as_uuid=True), ForeignKey("curso.id_curso"), nullable=False
    )


    monto = Column[float](Float, nullable=False)
    estado_pago = Column[str](String(20), nullable=True)
    metodo_pago = Column[str](String(50), nullable=True)

    fecha_pago = Column(DateTime(timezone=True), server_default=func.now())

    id_curso = Column(
        UUID(as_uuid=True), ForeignKey("curso.id_curso"), nullable=False
    )

    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )
    
    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )

    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita])

    curso = relationship("Curso", foreign_keys=[id_curso])
