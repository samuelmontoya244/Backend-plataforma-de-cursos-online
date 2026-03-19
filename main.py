"""
Punto de entrada: inicio de sesión (o creación del primer usuario)
y menú CRUD para Categoría, Producto y Pedido.
"""

import sys
from typing import Optional
from uuid import UUID

sys.path.insert(0, ".")

from src.services import categoria as services_categoria
from src.services import usuario as services_usuario
from src.services import curso as services_curso
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
    
def leer_int_positivo(mensaje: str) -> int:
    while True:
        valor = leer_int(mensaje)

        if valor is None:
            print("Este campo es obligatorio.")
            continue

        if valor <= 0:
            print("El valor debe ser mayor que 0.")
            continue

        return valor


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
        tipo_doc = leer_texto("Tipo documento: ")
        if not tipo_doc:
            print("Tipo de documento obligatorio.")
            return None
        doc_id = leer_texto("Documento de identidad: ")
        if not doc_id:
            print("Documento de identidad obligatorio.")
            return None
        email = leer_texto("Email: ")
        if not email:
            print("Email obligatorio.")
            return None
        contra = leer_texto("Contraseña: ")
        if not contra:
            print("Contraseña obligatoria.")
            return None
        rol = leer_texto("Rol (por defecto 'admin'): ") or "admin"
        try:
            usuario_creado = services_usuario.crear(
                nombre_usuario=nombre, tipo_documento=tipo_doc, documento_identidad=doc_id, email=email, contrasena=contra, rol=rol
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

def menu_categorias(usuario_id: UUID) -> None:
    while True:
        print("\n--- Categorías ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            for c in services_categoria.obtener_todos():
                print(f"  {c.id_categoria} | {c.nombre_categoria}")
        elif op == "2":
            nombre_categoria = leer_texto("Nombre categoría: ")
            if nombre_categoria:
                try:
                    services_categoria.crear(nombre_categoria, usuario_id or None)
                    print("Categoría creada.")
                except Exception as e:
                    print("Error:", e)
            else:
                print("Nombre obligatorio.")
        elif op == "3":
            id_cat = leer_uuid("ID categoría a actualizar: ")
            if not id_cat:
                print("ID inválido.")
                continue
            c = services_categoria.obtener_por_id(id_cat)
            if not c:
                print("No existe esa categoría.")
                continue
            nombre_categoria = leer_texto(f"Nuevo nombre (actual: {c.nombre_categoria}): ") or c.nombre_categoria
            services_categoria.actualizar(
                id_cat,
                usuario_id,
                nombre_categoria=nombre_categoria,
            )
            print("Actualizado.")
        elif op == "4":
            id_cat = leer_uuid("ID categoría a eliminar: ")
            if id_cat and services_categoria.eliminar(id_cat):
                print("Eliminada.")
            else:
                print("No se pudo eliminar (ID inválido o no existe).")


def menu_cursos(usuario_id: UUID) -> None:
    while True:
        print("\n--- Cursos ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            for c in services_curso.obtener_todos():

                if not services_curso.obtener_todos():
                    print("No hay cursos registrados.")
                    continue

                print(f"  {c.id_curso} | {c.nombre_curso}")

        elif op == "2":

            categorias = services_categoria.obtener_todos()

            if not categorias:
                print("No hay categorías creadas. Debes crear una primero.")
                continue

            print("Categorías disponibles:")
            for cat in categorias:
                print(f"  {cat.id_categoria} | {cat.nombre_categoria}")
                
            id_categoria = leer_uuid("ID categoría: ")
            if not id_categoria:
                print("ID categoría inválido.")
                continue
            nombre_curso = leer_texto("Nombre del curso: ")
            if not nombre_curso:
                print("Nombre del curso obligatorio.")
                continue
            descr = leer_texto("Descripción del curso (opcional): ")
            duracion = leer_int_positivo("Duración en horas: ")
            estado_curso = leer_texto("Estado del curso (Por defecto 'borrador'): ") or "borrador"
            if not estado_curso:
                print("Estado del curso obligatorio.")
                continue
            try:
                curso_creado = services_curso.crear(
                    id_categoria=id_categoria,
                    nombre_curso=nombre_curso,
                    duracion_horas=duracion,
                    estado_curso=estado_curso,
                    id_usuario_creacion=usuario_id,
                    descripcion_curso=descr
                )
                print(
                    f"\nCurso creado correctamente: {curso_creado.nombre_curso}"
                )
            except Exception as e:
                print("Error al crear curso:", e)
                return None
        elif op == "3":
            id_curso = leer_uuid("ID curso a actualizar: ")
            if not id_curso:
                print("ID inválido.")
                continue
            c = services_curso.obtener_por_id(id_curso)
            if not c:
                print("No existe ese curso.")
                continue
            nombre_curso = leer_texto(f"Nuevo nombre (actual: {c.nombre_curso}): ") or c.nombre_curso
            services_curso.actualizar(
                id_curso,
                usuario_id,
                nombre_curso=nombre_curso,
            )
            print("Actualizado.")
        elif op == "4":
            id_curso = leer_uuid("ID curso a eliminar: ")
            if id_curso and services_curso.eliminar(id_curso):
                print("Eliminado.")
            else:
                print("No se pudo eliminar (ID inválido o no existe).")

def main() -> None:
    usuario = ingresar_o_crear_usuario()
    if not usuario:
        print("No se pudo iniciar sesión. Saliendo.")
        return

    while True:
        print("\n========== Menú principal ==========")
        print("""
        1. Categorías
        2. Cursos
        3. Lecciones
        4. Material
        5. Evaluaciones
        6. Pagos
        7. Inscripciones
        8. Calificaciones
        9. Certificados

        0. Salir

==================================
        """)
        
        op = leer_texto("Opción: ")
        if op == "0":
            print(f"Hasta luego {usuario.nombre_usuario}.")
            break
        if op == "1":
            menu_categorias(usuario.id_usuario)
        elif op == "2":
            menu_cursos(usuario.id_usuario)
            
        #elif op == "3":

        #elif op == "4":
        
        #elif op == "5":

        #elif op == "6":

        #elif op == "7":

        #elif op == "8":

        #elif op == "9":
            
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()

