class cursos_de_programacion:
    def __init__(self, nombre, duracion, nivel):
        self.nombre = nombre
        self.duracion = duracion
        self.nivel = nivel

    def mostrar_informacion(self):
        print(f"Curso: {self.nombre}")
        print(f"Duración: {self.duracion} horas")
        print(f"Nivel: {self.nivel}")
