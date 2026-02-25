from src.entities.usuario import Usuario

class Instructor(Usuario):
    def __init__(
        self, 
        id_usuario: int         = None, 
        nombre: str             = None, 
        apellido: str           = None,  
        cedula: str             = None, 
        telefono: str           = None,
        especialidad: str       = None
    )-> None:
        
        super().__init__(id_usuario, nombre, apellido, cedula, telefono , especialidad)

    def get_especialidad(self) -> str:
        return self.__especialidad
    
    def set_especialidad(self, especialidad: str) -> None:
        self.__especialidad = especialidad

    