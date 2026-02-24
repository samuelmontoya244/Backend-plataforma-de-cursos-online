from datetime import date

class Usuario:
    def __init__(
        self,
        id_usuario: int        = None, 
        nombre: str            = None, 
        apellido: str          = None,  
        cedula: str            = None, 
        telefono: str          = None
    )-> None:
        self.__id_usuario = id_usuario
        self.__nombre = nombre
        self.__apellido = apellido
        self.__cedula = cedula
        self.__telefono = telefono
    
    def get_id_usuario(self) -> int:
        return self.__id_usuario
    
    def get_nombre(self) -> str:
        return self.__nombre
    
    def get_apellido(self) -> str:
        return self.__apellido
    
    def get_cedula(self) -> str:
        return self.__cedula
    
    def get_telefono(self) -> str:
        return self.__telefono
    
    def set_id_usuario(self, id_usuario: int) -> None:
        self.__id_usuario = id_usuario
    
    def set_nombre(self, nombre: str) -> None:
        self.__nombre = nombre

    def set_apellido(self, apellido: str) -> None:
        self.__apellido = apellido

    def set_cedula(self, cedula: str) -> None:
        self.__cedula = cedula

    def set_telefono(self, telefono: str) -> None:
        self.__telefono = telefono
    
    #Para facilitar la impresión de los datos del usuario
    def __str__(self):
        return (f"ID: {self.__id_usuario},"
                f"{self.__nombre} {self.__apellido},"
                f"Cédula: {self.__cedula},"
                f"Tel: {self.__telefono}")