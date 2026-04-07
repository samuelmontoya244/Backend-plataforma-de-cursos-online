# Modelos de respuesta para la API
from typing import Optional
from pydantic import BaseModel

class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool = True
    datos: Optional[dict] = None