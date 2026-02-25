from src.entities.instructor import Instructor


class Curso:

    def __init__(
        self,
        codigo: int = None,
        nombre: str = None,
        categoria: str = None,
        duracionhoras: int = None,
        instructor: Instructor = None,
    ):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__categoria = categoria
        self.__duracionhoras = duracionhoras
        self.__instructor = instructor

    def get_codigo(self) -> int:
        return self.__codigo

    def get_nombre(self) -> str:
        return self.__nombre

    def get_categoria(self) -> str:
        return self.__categoria

    def get_duracionhoras(self) -> int:
        return self.__duracionhoras

    def get_instructor(self) -> Instructor:
        return self.__instructor

    def set_codigo(self, codigo: int) -> None:
        self.__codigo = codigo

    def set_nombre(self, nombre: str) -> None:
        self.__nombre = nombre

    def set_categoria(self, categoria: str) -> None:
        self.__categoria = categoria

    def set_duracionhoras(self, duracionhoras: int) -> None:
        self.__duracionhoras = duracionhoras

    def set_instructor(self, instructor: Instructor) -> None:
        self.__instructor = instructor

    def __str__(self) -> str:
        return f"{self.__codigo}, {self.__nombre}, {self.__categoria}, {self.__duracionhoras}, {self.__instructor}"
