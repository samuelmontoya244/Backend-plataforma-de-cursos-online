from datetime import datetime
from typing import Optional
from uuid import UUID


from pydantic import BaseModel, EmailStr, ConfigDict

class UsuarioCreate(BaseModel):
    nombre_usuario: str
    tipo_documento: str
    documento_identidad: str
    email: EmailStr
    contrasena: str
    rol: str
    activo: bool = True


class UsuarioUpdate(BaseModel):
    nombre_usuario: Optional[str] = None
    tipo_documento: Optional[str] = None
    documento_identidad: Optional[str] = None
    email: Optional[EmailStr] = None
    contrasena: Optional[str] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None


class UsuarioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_usuario: UUID
    nombre_usuario: str
    tipo_documento: str
    documento_identidad: str
    email: str
    rol: str
    activo: bool

class UsuarioResponse(BaseModel):
    id_usuario: UUID
    nombre_usuario: str
    activo: bool
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    nombre_usuario: str
    contraseña: str

# Modelos de respuesta para la API
class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool = True
    datos: Optional[dict] = None