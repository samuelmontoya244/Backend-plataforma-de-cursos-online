from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class  CalificacionCreate(BaseModel):
     id_inscripcion: UUID
     id_evaluacion: UUID
     Nota: float

class CalificacionUpdate(BaseModel):
    Nota: Optional[float] = None
   

class CalificacionResponse(BaseModel):
    id_inscripcion: UUID
    id_evaluacion: UUID
    Nota: float
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None


    class Config:
        from_attributes = True