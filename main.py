"""
Punto de entrada: inicio de sesión (o creación del primer usuario)
y menú CRUD para Categoría, Producto y Pedido.
"""

import sys
from typing import Optional
from uuid import UUID

sys.path.insert(0, ".")

#from src.services import categoria as services_categoria
from src.services import usuario as services_usuario
from src.entities.usuario import Usuario


def leer_texto(mensaje: str, default: str = "") -> str:
    s = input(mensaje).strip()
    return s if s else default


def leer_float(mensaje: str, default: float = 0.0) -> float:
    try:
        return float(input(mensaje).strip() or default)
    except ValueError:
        return default


def leer_int(mensaje: str, default: int = 0) -> int:
    try:
        return int(input(mensaje).strip() or default)
    except ValueError:
        return default


def leer_uuid(mensaje: str) -> Optional[UUID]:
    s = input(mensaje).strip()
    if not s:
        return None
    try:
        return UUID(s)
    except ValueError:
        return None


def ingresar_o_crear_usuario() -> Optional[Usuario]:
    """
    Si no hay usuarios, ofrece crear el primero.
    Luego pide login hasta que sea correcto.
    Devuelve el Usuario logueado.
    """
    if not services_usuario.hay_usuarios():
        print("\n--- No hay usuarios en el sistema ---")
        print("Crea el primer usuario para poder entrar.\n")
        nombre = leer_texto("Nombre de usuario: ")
        if not nombre:
            print("Nombre obligatorio.")
            return None
        contra = leer_texto("Contraseña: ")
        if not contra:
            print("Contraseña obligatoria.")
            return None
        rol = leer_texto("Rol (por defecto 'admin'): ") or "admin"
        try:
            usuario_creado = services_usuario.crear(
                nombre_usuario=nombre, contrasena=contra, rol=rol
            )
            print(
                f"\nUsuario '{usuario_creado.nombre_usuario}' creado. Inicia sesión.\n"
            )
        except Exception as e:
            print("Error al crear usuario:", e)
            return None

    while True:
        print("--- Inicio de sesión ---")
        nombre = leer_texto("Usuario: ")
        contra = leer_texto("Contraseña: ")
        if not nombre or not contra:
            print("Usuario y contraseña obligatorios.\n")
            continue
        usuario = services_usuario.login(nombre, contra)
        if usuario:
            print(f"\nBienvenido, {usuario.nombre_usuario} ({usuario.rol}).\n")
            return usuario
        print("Usuario o contraseña incorrectos.\n")

