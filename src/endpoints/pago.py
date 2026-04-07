from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from .deps import DbSession

from src.services import pago as services_pago
from src.schemas.response_schema import RespuestaAPI
from src.schemas.pago_schema import (
    PagoCreate,
    PagoUpdate,
    PagoResponse,
)

router = APIRouter(prefix="/pago", tags=["pagos"])


@router.get("", response_model=List[PagoResponse])
def listar_pagos(db: DbSession, skip: int = 0, limit: int = 100) -> List[PagoResponse]:
    pago = services_pago.listar(db, skip=skip, limit=limit)
    return pago

@router.get("/{id_pago}", response_model=PagoResponse)
def obtener_pago(id_pago: UUID, db: DbSession) -> PagoResponse:
    db_pago = services_pago.obtener_por_id(db, id_pago)
    if not db_pago:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"El pago con ID {id_pago} no existe en la base de datos"
        )
    return db_pago


@router.post("", response_model=PagoResponse, status_code=status.HTTP_201_CREATED)
def crear_pago(db: DbSession, dato: PagoCreate):

    try:
        pago = services_pago.crear(
            db,
            id_usuario=dato.id_usuario,
            id_usuario_creacion=dato.id_usuario_creacion,
            id_curso=dato.id_curso,
            monto=dato.monto,
            estado_pago=dato.estado_pago,
            metodo_pago=dato.metodo_pago
        )
        return pago

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{id_pago}", response_model=PagoResponse)
def actualizar_pago(id_pago: UUID, dato: PagoUpdate, db: DbSession):

    pago = services_pago.actualizar(
        db,
        id_pago,
        **dato.model_dump(exclude_unset=True)
    )

    if not pago:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pago no encontrado"
        )

    return pago


@router.delete("/{id_pago}", response_model=RespuestaAPI)
def eliminar_pago(id_pago: UUID, db: DbSession) -> None:
    try:
        # Verificar que el usuario existe
        usuario_existente = services_pago.obtener_por_id(db,id_pago)
        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado"
            )

        eliminado = services_pago.eliminar(db, id_pago)
        if eliminado:
            return RespuestaAPI(mensaje="Pago eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar pago",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar pago: {str(e)}",
        )