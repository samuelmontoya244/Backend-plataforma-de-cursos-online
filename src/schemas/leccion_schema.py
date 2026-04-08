from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class  LeccionCreate(BaseModel):
     id_usuario_creacion: UUID
     id_curso: UUID
     titulo_leccion: str    
     descripcion_leccion: Optional[str]
     orden: int
     duracion_horas: int


class LeccionUpdate(BaseModel):
    id_usuario_edita: UUID 
    id_curso: Optional[UUID] = None
    titulo_leccion: Optional[str] = None
    descripcion_leccion: Optional[str] = None
    orden: Optional[int] = None
    duracion_horas: Optional[int] = None 

class LeccionResponse(BaseModel):
    id_curso: UUID
    id_leccion: UUID
    titulo_leccion: str = None
    descripcion_leccion: Optional[str] = None
    orden: int = None
    duracion_horas: int = None
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None


    class Config:
        from_attributes = True 