from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

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

class UsuarioResponse(BaseModel):
    id_usuario: UUID
    nombre_usuario: str
    tipo_documento: str
    documento_identidad: str
    email: EmailStr
    rol: str
    activo: bool
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    nombre_usuario: str
    contrasena: str