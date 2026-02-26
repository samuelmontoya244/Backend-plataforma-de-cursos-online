from src.entities.estudiante import Estudiante
from src.entities.curso import Curso
from src.entities.instructor import Instructor
from src.entities.inscripciones import Inscripciones
from datetime import date


class Plataforma:

    def __init__(self) -> None:
        self.__estudiantes = []
        self.__cursos = []
        self.__instructores = []
        self.__inscripciones = []
        self.__contador_id = 1

    @property
    def estudiantes(self):
        return self.__estudiantes
    
    @property
    def cursos(self):
        return self.__cursos
    
    @property
    def instructores(self):
        return self.__instructores
    
    @property
    def inscripciones(self):
        return self.__inscripciones

    def existe_estudiante(self, cedula):
        for est in self.__estudiantes:
            if str(est.get_cedula()) == str(cedula):
                return True
        return False

    def existe_instructor(self, cedula):
        for inst in self.__instructores:
            if str(inst.get_cedula()) == str(cedula):
                return True
        return False

    def existe_curso(self, codigo):
        for c in self.__cursos:
            if str(c.get_codigo()) == str(codigo):
                return True
        return False

    def crear_estudiante(self, cedula, nombre, email, telefono) -> Estudiante:
        for est in self.__estudiantes:
            if str(est.get_cedula()) == str(cedula):
                raise ValueError(f"Ya existe un estudiante con la cédula {cedula}")
        
        nuevo_estudiante = Estudiante(self.__contador_id, nombre, nombre, cedula, telefono)
        self.__estudiantes.append(nuevo_estudiante)
        self.__contador_id += 1
        return nuevo_estudiante

    def crear_instructor(self, cedula, nombre, email, telefono, especialidad="General") -> Instructor:
        for inst in self.__instructores:
            if str(inst.get_cedula()) == str(cedula):
                raise ValueError(f"Ya existe un instructor con la cédula {cedula}")
        
        nuevo_instructor = Instructor(self.__contador_id, nombre, nombre, cedula, telefono, especialidad)
        self.__instructores.append(nuevo_instructor)
        self.__contador_id += 1
        return nuevo_instructor

    def crear_curso(self, codigo, nombre, descripcion, instructor: Instructor) -> Curso:
        for c in self.__cursos:
            if str(c.get_codigo()) == str(codigo):
                raise ValueError(f"Ya existe un curso con el código {codigo}")
        
        nuevo_curso = Curso(codigo, nombre, descripcion, 40, instructor)
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

    def inscribir_estudiante(self, estudiante: Estudiante, curso: Curso) -> None:
        if estudiante not in self.__estudiantes or curso not in self.__cursos:
            raise ValueError("El estudiante o el curso no existen en la plataforma.")
        
        for inscripcion in self.__inscripciones:
            if inscripcion.get_estudiante() == estudiante and inscripcion.get_curso() == curso:
                raise ValueError("El estudiante ya está inscrito en este curso.")
        
        nueva_inscripcion = Inscripciones(
            fecha_inscripcion=date.today(),
            estudiante=estudiante,
            curso=curso
        )
        self.__inscripciones.append(nueva_inscripcion)
        
    def calificar_estudiante(self, inscripcion, nota_final):
        if inscripcion in self.__inscripciones:
            inscripcion.registrar_calificacion(nota_final)
            return True
        return False
    
    def emitir_certificado(self, inscripcion):
        if inscripcion in self.__inscripciones and inscripcion.get_nota_final() and inscripcion.get_nota_final() >= 3.0:
            inscripcion.set_estado(True)
            return True
        return False