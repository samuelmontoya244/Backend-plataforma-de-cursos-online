from src.entities.usuario import Usuario

class Estudiante(Usuario):
    def __init__(
        self, 
        id_usuario: int        = None, 
        nombre: str            = None, 
        apellido: str          = None,  
        cedula: str            = None, 
        telefono: str          = None
    )-> None:
        
        super().__init__(id_usuario, nombre, apellido, cedula, telefono)