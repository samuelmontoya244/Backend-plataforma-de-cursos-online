from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.calificacion import Calificacion
from src.entities.inscripcion import Inscripcion, EstadoInscripcion

db = SessionLocal()

TOTAL_EVALUACIONES_REQUERIDAS = 4
NOTA_MINIMA_APROBACION = 3.0

def _actualizar_estado_inscripcion(id_inscripcion: UUID) -> None:
    """
    Verifica si ya hay 4 calificaciones para la inscripción.
    Si las hay, suma las notas y actualiza el estado de la inscripción.
    """
    calificaciones = (
        db.query(Calificacion)
        .filter(Calificacion.id_inscripcion == id_inscripcion)
        .all()
    )

    inscripcion = db.query(Inscripcion).filter(
        Inscripcion.id_inscripcion == id_inscripcion
    ).first()

    if not inscripcion:
        raise ValueError("La inscripción no existe.")

    if len(calificaciones) < TOTAL_EVALUACIONES_REQUERIDAS:
        faltantes = TOTAL_EVALUACIONES_REQUERIDAS - len(calificaciones)
        raise ValueError(
            f"Faltan {faltantes} Nota(s) para completar las "
            f"{TOTAL_EVALUACIONES_REQUERIDAS} evaluaciones requeridas."
        )

    suma = sum(c.Nota for c in calificaciones)

    if suma >= NOTA_MINIMA_APROBACION:
        inscripcion.estado_inscripcion = EstadoInscripcion.APROBADA
    else:
        inscripcion.estado_inscripcion = EstadoInscripcion.REPROBADA

    db.commit()

def crear(
    id_inscripcion: UUID,
    id_evaluacion: UUID,
    Nota: float,
    id_usuario_creacion: UUID,
) -> Calificacion:
    
    if not (0 <= Nota <= 5):
        raise ValueError("La Nota debe estar entre 0 y 5")

    
    existente = obtener_por_id(id_inscripcion, id_evaluacion)
    if existente:
        raise ValueError(
            "Ya existe una calificación para esta inscripción y evaluación."
        )

    
    total_actuales = (
        db.query(Calificacion)
        .filter(Calificacion.id_inscripcion == id_inscripcion)
        .count()
    )
    if total_actuales >= TOTAL_EVALUACIONES_REQUERIDAS:
        raise ValueError(
            f"Esta inscripción ya tiene las "
            f"{TOTAL_EVALUACIONES_REQUERIDAS} evaluaciones registradas."
        )

    calificacion = Calificacion(
        id_inscripcion=id_inscripcion,
        id_evaluacion=id_evaluacion,
        Nota=Nota,
        id_usuario_creacion=id_usuario_creacion,
    )
    db.add(calificacion)
    db.commit()
    db.refresh(calificacion)

    
    total_tras_crear = total_actuales + 1
    if total_tras_crear == TOTAL_EVALUACIONES_REQUERIDAS:
        _actualizar_estado_inscripcion(id_inscripcion)

    return calificacion

def obtener_por_id(
    id_inscripcion: UUID, id_evaluacion: UUID
) -> Optional[Calificacion]:
    return (
        db.query(Calificacion)
        .filter(
            Calificacion.id_inscripcion == id_inscripcion,
            Calificacion.id_evaluacion == id_evaluacion,
        )
        .first()
    )

def obtener_todos() -> List[Calificacion]:
    return db.query(Calificacion).all()

def obtener_por_inscripcion(id_inscripcion: UUID) -> List[Calificacion]:
    return (
        db.query(Calificacion)
        .filter(Calificacion.id_inscripcion == id_inscripcion)
        .all()
    )

def actualizar(
    id_inscripcion: UUID,
    id_evaluacion: UUID,
    id_usuario_edita: UUID,
    **kwargs: dict,
) -> Optional[Calificacion]:
    calificacion = obtener_por_id(id_inscripcion, id_evaluacion)
    if not calificacion:
        return None

    if "Nota" in kwargs and not (0 <= kwargs["Nota"] <= 5):
        raise ValueError("La Nota debe estar entre 0 y 5.")

    for key, value in kwargs.items():
        setattr(calificacion, key, value)
    calificacion.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(calificacion)

    total = (
        db.query(Calificacion)
        .filter(Calificacion.id_inscripcion == id_inscripcion)
        .count()
    )
    if total == TOTAL_EVALUACIONES_REQUERIDAS:
        _actualizar_estado_inscripcion(id_inscripcion)

    return calificacion

def eliminar(id_inscripcion: UUID, id_evaluacion: UUID) -> bool:
    calificacion = obtener_por_id(id_inscripcion, id_evaluacion)
    if not calificacion:
        return False
    db.delete(calificacion)
    db.commit()
    return True

