from src.entities.estudiante import Estudiante
from src.entities.curso import Curso
from src.entities.instructor import Instructor
from src.entities.inscripciones import Inscripciones


class Plataforma:

    def __init__(self) -> None:
        self.__estudiantes = []
        self.__cursos = []
        self.__instructores = []
        self.__inscripciones = []

    def crear_estudiante(
        self,
        id_usuario: int,
        nombre: str,
        apellido: str,
        cedula: int,
        telefono: int,
    ) -> Estudiante:

        for est in self.__estudiantes:
            if est.cedula == cedula:
                raise ValueError(f"Ya existe un estudiante con la cédula {cedula}")

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

    def obtener_estudiante_por_id(self, id_usuario):
        for e in self.__estudiantes:
            if e.get_id_usuario() == id_usuario:
                return e
        return None

    def obtener_curso_por_codigo(self, codigo):
        for c in self.__cursos:
            if c.get_codigo() == codigo:
                return c
        return None

    def obtener_instructor_por_id(self, id_usuario):
        for i in self.__instructores:
            if i.get_id_usuario() == id_usuario:
                return i
        return None

    def inscribir_estudiante_a_curso(
        self, estudiante: Estudiante, curso: Curso
    ) -> None:
        if estudiante in self.__estudiantes and curso in self.__cursos:
            nueva_inscripcion = Inscripciones(estudiante=estudiante, curso=curso)
            self.__inscripciones.append(nueva_inscripcion)
            print(f"Éxito: {estudiante.get_nombre()} inscrito en {curso.get_nombre()}.")
        else:
            raise ValueError("El estudiante o el curso no existen en la plataforma.")

    def calificar_estudiante(self, estudiante, curso, nota_final):
        for inscripcion in self.__inscripciones:
            if (
                inscripcion.get_estudiante() == estudiante
                and inscripcion.get_curso() == curso
            ):
                inscripcion.registrar_calificacion(nota_final)
                return True
        return False

    def emitir_certificado(self, estudiante, curso):
        for inscripcion in self.__inscripciones:
            if (
                inscripcion.get_estudiante() == estudiante
                and inscripcion.get_curso() == curso
            ):
                if inscripcion.get_estado():
                    return f"Certificado: {estudiante.get_nombre()} ha completado el curso {curso.get_nombre()} con una nota final de {inscripcion.get_nota_final()}."
                else:
                    return f"El estudiante {estudiante.get_nombre()} no ha aprobado el curso {curso.get_nombre()}."
        return "No se encontró la inscripción para el estudiante y curso especificados."
