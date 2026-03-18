import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func

from src.database.config import Base


class Categoria(Base):

    __tablename__ = "categoria"

    id_categoria = Column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre_categoria = Column(String(150), nullable=False, unique=True)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())


class CategoriaBase(BaseModel):

    nombre_categoria: str = Field(..., min_length=1, max_length=150)


class CategoriaCreate(CategoriaBase):

    pass


class CategoriaUpdate(BaseModel):

    nombre_categoria: Optional[str] = Field(None, min_length=1, max_length=150)


class CategoriaResponse(CategoriaBase):

    id_categoria: UUID
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True
