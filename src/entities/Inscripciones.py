from src.entities.estudiante import Estudiante
from src.entities.curso import Curso
from datetime import date


class Inscripciones:
    def __init__(
        self,
        fecha_inscripcion: date = None,
        nota_final: float = None,
        estado: bool = None,
        estudiante: Estudiante = None,
        curso: Curso = None,
    ):
        self.__fecha_inscripcion = fecha_inscripcion
        self.__nota_final = nota_final
        self.__estado = estado
        self.__estudiante = estudiante
        self.__curso = curso

    def get_fecha_inscripcion(self) -> date:
        return self.__fecha_inscripcion

    def get_nota_final(self) -> float:
        return self.__nota_final

    def get_estado(self) -> bool:
        return self.__estado

    def get_estudiante(self) -> Estudiante:
        return self.__estudiante

    def get_curso(self) -> Curso:
        return self.__curso

    def set_fecha_inscripcion(self, fecha_inscripcion: date) -> None:
        self.__fecha_inscripcion = fecha_inscripcion

    def set_nota_final(self, nota_final: float) -> None:
        self.__nota_final = nota_final

    def set_estado(self, estado: bool) -> None:
        self.__estado = estado

    def set_estudiante(self, estudiante: Estudiante) -> None:
        self.__estudiante = estudiante

    def set_curso(self, curso: Curso) -> None:
        self.__curso = curso

    def registrar_calificacion(self, nota: float):
        self.__nota_final = nota
        self.__estado = (nota >= 3.0)

    def __str__(self) -> str:
        return f"{self.__fecha_inscripcion}, {self.__nota_final}, {self.__estado}, {self.__estudiante}, {self.__curso}"
