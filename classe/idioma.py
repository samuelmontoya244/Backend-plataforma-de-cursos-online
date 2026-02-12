class idioma:
    def __init__(self, idioma:str, nivel:str, dificultad:int, estado:str):
        self.nivel = nivel
        self.dificultad = dificultad
        self.estado = estado
        self.idioma = idioma

    def __str__(self):
        return f"Idioma: {self.idioma}, Nivel: {self.nivel}, Dificultad: {self.dificultad}, Estado: {self.estado}"