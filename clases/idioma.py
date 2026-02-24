class idioma:
    def __init__(self, nombre: str, nivel: str, dificultad: str, horas: int, id: int):
        self._nombre = nombre
        self._nivel = nivel
        self._dificultad = dificultad
        self._horas = horas
        self._id = id

    def get_nombre(self) -> str:
        return self._nombre

    def get_nivel(self) -> str:
        return self._nivel

    def get_dificultad(self) -> str:
        return self._dificultad

    def get_horas(self) -> int:
        return self._horas

    def get_id(self) -> int:
        return self._id

    def set_nombre(self, nombre) -> None:
        self._nombre = nombre

    def set_nivel(self, nivel) -> None:
        self._nivel = nivel

    def set_dificultad(self, dificultad) -> None:
        self._dificultad = dificultad

    def set_horas(self, horas) -> None:
        self._horas = horas

    def set_id(self, id) -> None:
        self._id = id

    def validar_nombre(self, nombre) -> bool:
        if nombre in ["python", "SQL", "java", "java_script", "c++", "html"]:
            return True
        else:
            return False

    def __str__(self):
        return f"Nombre: {self._nombre}, Nivel: {self._nivel}, Dificultad: {self._dificultad}, Horas: {self._horas}, Id: {self._id}"
