from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class MaterialCreate(BaseModel):
    id_usuario_creacion: UUID
    id_leccion: UUID
    titulo_material: str
    tipo_material: str
    URL_archivo: str


class MaterialUpdate(BaseModel):
    id_usuario_creacion: Optional[UUID] = None
    id_leccion: Optional[UUID] = None
    titulo_material: Optional[str] = None
    tipo_material: Optional[str] = None
    URL_archivo: Optional[str] = None


class MaterialRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_usuario:UUID
    id_usuario_creacion: UUID
    id_leccion: UUID
    titulo_material: str = None
    tipo_material: str | None = None
    URL_archivo: str = None
 

class MaterialResponse(BaseModel):
    id_usuario:UUID
    id_usuario_creacion: UUID
    id_leccion: UUID
    titulo_material: str = None
    tipo_material: str | None = None
    URL_archivo: str = None
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True

# Modelos de respuesta para la API
class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool = True
    datos: Optional[dict] = None