from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class  leccionCreate(BaseModel):
     id_usuario_creacion: UUID
     id_curso: UUID
     titulo_leccion: str
     descripcion_leccion: str
     orden: int
     duracion_horas: int


class LeccionUpdate(BaseModel):
    id_usuario_creacion: Optional[UUID] = None
    id_leccion: Optional[UUID] = None
    titulo_leccion: Optional[str] = None
    descripcion_leccion: Optional[str] = None
    orden: Optional[int] = None
    duracion_horas: Optional[int] = None


class LeccionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_usuario:UUID
    id_usuario_creacion: UUID
    id_leccion: UUID
    titulo_leccion: str = None
    descripcion_leccion: str | None = None
    orden: int = None
    duracion_horas: int = None
 

class LeccionResponse(BaseModel):
    
    id_usuario:UUID
    id_usuario_creacion: UUID
    id_leccion: UUID
    titulo_leccion: str = None
    descripcion_leccion: str | None = None
    orden: int = None
    duracion_horas: int = None
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None


    class Config:
        from_attributes = True

# Modelos de respuesta para la API
class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool = True
    datos: Optional[dict] = None