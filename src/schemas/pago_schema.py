from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class PagoCreate(BaseModel):
    id_usuario: UUID
    id_usuario_creacion: UUID
    id_curso: UUID
    monto: float
    estado_pago: str
    metodo_pago: str


class PagoUpdate(BaseModel):
    id_usuario: Optional[UUID] = None
    id_usuario_creacion: Optional[UUID] = None
    id_curso: Optional[UUID] = None
    monto: Optional[float] = None
    estado_pago: Optional[str] = None
    metodo_pago: Optional[str] = None

class PagoResponse(BaseModel):
    id_usuario:UUID
    id_usuario_creacion: UUID
    id_curso: UUID 
    monto: float = None
    estado_pago: str = None
    metodo_pago: str = None
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True