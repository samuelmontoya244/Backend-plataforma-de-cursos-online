from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from .deps import DbSession

from src.services import certificado as services_certificado
from src.schemas.response_schema import RespuestaAPI
from src.schemas.certificado_schema import (
    CertificadoCreate,
    CertificadoUpdate,
    CertificadoResponse,
)

router = APIRouter(prefix="/certificados", tags=["certificados"])


@router.get("", response_model=List[CertificadoResponse])
def listar_certificados(db: DbSession, skip: int = 0, limit: int = 100):
    certificados = services_certificado.obtener_todos(db, skip, limit)
    return certificados


@router.get("/{id_certificado}", response_model=CertificadoResponse)
def obtener_certificado(db: DbSession, id_certificado: UUID) -> CertificadoResponse:
    db_certificado = services_certificado.obtener_por_id(db, id_certificado)
    if not db_certificado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El certificado con ID {id_certificado} no existe en la base de datos",
        )
    return db_certificado


@router.post(
    "", response_model=CertificadoResponse, status_code=status.HTTP_201_CREATED
)
def crear_certificado(db: DbSession, dato: CertificadoCreate):

    try:
        Certificado = services_certificado.crear(
            db,
            id_inscripcion=dato.id_inscripcion,
            id_usuario_creacion=dato.id_usuario_creacion,
        )
        return Certificado

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{id_certificado}", response_model=CertificadoResponse)
def actualizar_certificado(
    db: DbSession, id_certificado: UUID, dato: CertificadoUpdate
):

    certificado = services_certificado.actualizar(
        db, id_certificado, **dato.model_dump(exclude_unset=True)
    )

    if not certificado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Certificado no encontrado"
        )

    return certificado


@router.delete("/{id_certificado}", response_model=RespuestaAPI)
def eliminar_certificado(db: DbSession, id_certificado: UUID):
    try:
        certificado_existente = services_certificado.obtener_por_id(db, id_certificado)
        if not certificado_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Certificado no encontrado",
            )

        eliminado = services_certificado.eliminar(db, id_certificado)
        if eliminado:
            return RespuestaAPI(
                mensaje="Certificado eliminado exitosamente", exito=True
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar certificado",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar certificado: {str(e)}",
        )
