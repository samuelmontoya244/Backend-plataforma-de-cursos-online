from src.entities.estudiante import Estudiante
from src.entities.curso import Curso
from src.entities.instructor import Instructor


class Plataforma:

    def __init__(self) -> None:
        self.__estudiantes = []
        self.__cursos = []
        self.__instructores = []

    def crear_estudiante(
        self,
        id_usuario: int,
        nombre: str,
        apellido: str,
        cedula: int,
        telefono: int,
    ) -> None:
        nuevo_estudiante = Estudiante(id_usuario, nombre, apellido, cedula, telefono)
        self.__estudiantes.append(nuevo_estudiante)
        return nuevo_estudiante

    def crear_instructor(
        self,
        id_usuario: int,
        nombre: str,
        apellido: str,
        cedula: str,
        telefono: str,
        especialidad: str,
    ) -> None:
        nuevo_instructor = Instructor(
            id_usuario, nombre, apellido, cedula, telefono, especialidad
        )
        self.__instructores.append(nuevo_instructor)
        return nuevo_instructor

    def crear_curso(
        self,
        codigo: int,
        nombre: str,
        categoria: str,
        duracionhoras: int,
        instructor: Instructor,
    ) -> None:
        nuevo_curso = Curso(codigo, nombre, categoria, duracionhoras, instructor)
        self.__cursos.append(nuevo_curso)
        return nuevo_curso
