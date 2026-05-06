from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class EvaluacionCreate(BaseModel):
    id_leccion: UUID
    nombre_evaluacion: str
    porcentaje: float
    


class EvaluacionUpdate(BaseModel):
    id_leccion: Optional[UUID] = None
    nombre_evaluacion: Optional[str] = None
    porcentaje: Optional[float] = None
    


class EvaluacionResponse(BaseModel):
    id_evaluacion: UUID
    id_leccion: UUID
    nombre_evaluacion: str
    porcentaje: float
    id_usuario_creacion: UUID
    id_usuario_edita: Optional[UUID] = None
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True