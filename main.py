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
from src.services import material as service_material
from src.services import leccion as service_leccion
from src.services import evaluacion as service_evaluacion
from src.services import pago as service_pago
from src.services import inscripcion as services_inscripcion
from src.entities.usuario import Usuario
from src.services import calificacion as services_calificacion
from src.services import certificado as services_certificado
from src.entities.certificado import Certificado 


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
                nombre_usuario=nombre,
                tipo_documento=tipo_doc,
                documento_identidad=doc_id,
                email=email,
                contrasena=contra,
                rol=rol,
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
            nombre_categoria = (
                leer_texto(f"Nuevo nombre (actual: {c.nombre_categoria}): ")
                or c.nombre_categoria
            )
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

                print(
                    f"  {c.id_curso} | {c.nombre_curso}"
                    + (
                        f" | Categoría: {c.categoria.nombre_categoria}"
                        if c.categoria
                        else ""
                    )
                )

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
            estado_curso = (
                leer_texto("Estado del curso (Por defecto 'borrador'): ") or "borrador"
            )
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
                    descripcion_curso=descr,
                )
                print(f"\nCurso creado correctamente: {curso_creado.nombre_curso}")
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
            nombre_curso = (
                leer_texto(f"Nuevo nombre (actual: {c.nombre_curso}): ")
                or c.nombre_curso
            )
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


def menu_material(usuario_id: UUID) -> None:
    while True:
        print("\n--- Materiales ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opcion: ")
        if op == "0":
            return

        if op == "1":
            materiales = service_material.obtener_todos()
            if not materiales:
                print("No hay materiales registrados.")
            for c in materiales:
                print(
                    f"  {c.id_material} | {c.titulo_material} | {c.tipo_material} | {c.URL_archivo} | {c.id_leccion}"
                )

        elif op == "2":
            titulo_material = leer_texto("Nombre material: ")
            tipo_material = leer_texto("Tipo de material: ")
            URL_archivo = leer_texto("URL del archivo: ")
            id_leccion = leer_uuid("ID de la leccion: ")

            if not id_leccion or not service_leccion.obtener_por_id(id_leccion):
                print("Error: La leccion no existe o el ID es invalido.")
                continue

            if titulo_material and URL_archivo:
                try:

                    service_material.crear(
                        id_usuario_creacion=usuario_id,
                        id_leccion=id_leccion,
                        titulo_material=titulo_material,
                        tipo_material=tipo_material,
                        URL_archivo=URL_archivo,
                    )
                    print("Material creado.")
                except Exception as e:
                    print(f"Error al crear: {e}")
            else:
                print("Todos los campos son obligatorios.")

        elif op == "3":
            id_mat = leer_uuid("ID material a actualizar: ")
            if not id_mat:
                continue

            c = service_material.obtener_por_id(id_mat)
            if not c:
                print("No existe ese material.")
                continue

            titulo = (
                leer_texto(f"Nuevo titulo (actual: {c.titulo_material}): ")
                or c.titulo_material
            )
            tipo = (
                leer_texto(f"Nuevo tipo (actual: {c.tipo_material}): ")
                or c.tipo_material
            )
            url = leer_texto(f"Nueva URL (actual: {c.URL_archivo}): ") or c.URL_archivo

            nuevo_id_lec = leer_uuid(f"Nuevo ID de leccion (actual: {c.id_leccion}): ")
            id_leccion_final = (
                nuevo_id_lec
                if nuevo_id_lec and service_leccion.obtener_por_id(nuevo_id_lec)
                else c.id_leccion
            )

            try:

                service_material.actualizar(
                    id_material=id_mat,
                    id_usuario_edita=usuario_id,
                    titulo_material=titulo,
                    tipo_material=tipo,
                    URL_archivo=url,
                    id_leccion=id_leccion_final,
                )
                print("Actualizado.")
            except Exception as e:
                print(f"Error: {e}")

        elif op == "4":
            id_mat = leer_uuid("ID material a eliminar: ")
            if id_mat and service_material.eliminar(id_mat):
                print("Eliminado.")
            else:
                print("No se pudo eliminar.")


def menu_leccion(usuario_id: UUID) -> None:
    while True:
        print("\n--- Lecciones ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opcion: ")
        if op == "0":
            return

        if op == "1":
            for c in service_leccion.obtener_todos():
                print(
                    f"  {c.id_leccion} | {c.titulo_leccion} | {c.orden} | {c.id_curso}"
                )

        elif op == "2":
            titulo = leer_texto("Nombre de la leccion: ")
            desc = leer_texto("Descripcion: ")
            orden = leer_int("Orden: ")
            duracion = leer_float("Duracion (horas): ")
            id_curso = leer_uuid("ID del curso: ")

            if not id_curso or not services_curso.obtener_por_id(id_curso):
                print("Error: El curso no existe o el ID es invalido.")
                continue

            try:

                service_leccion.crear(
                    id_usuario_creacion=usuario_id,
                    id_curso=id_curso,
                    titulo_leccion=titulo,
                    descripcion_leccion=desc,
                    orden=orden,
                    duracion_horas=duracion,
                )
                print("Leccion creada correctamente.")
            except Exception as e:
                print(f"Error en la base de datos: {e}")

        elif op == "3":
            id_lec = leer_uuid("ID leccion a actualizar: ")
            if not id_lec:
                continue
            c = service_leccion.obtener_por_id(id_lec)
            if not c:
                print("No existe esa leccion.")
                continue

            titulo = (
                leer_texto(f"Nuevo titulo (actual: {c.titulo_leccion}): ")
                or c.titulo_leccion
            )
            desc = (
                leer_texto(f"Nueva desc (actual: {c.descripcion_leccion}): ")
                or c.descripcion_leccion
            )
            ord_n = leer_int(f"Nuevo orden (actual: {c.orden}): ") or c.orden
            dur = (
                leer_float(f"Nueva duracion (actual: {c.duracion_horas}): ")
                or c.duracion_horas
            )

            try:
                service_leccion.actualizar(
                    id_leccion=id_lec,
                    id_usuario_edita=usuario_id,
                    titulo_leccion=titulo,
                    descripcion_leccion=desc,
                    orden=ord_n,
                    duracion_horas=dur,
                    id_curso=c.id_curso,
                )
                print("Actualizado.")
            except Exception as e:
                print(f"Error: {e}")

        elif op == "4":
            id_lec = leer_uuid("ID leccion a eliminar: ")
            if id_lec and service_leccion.eliminar(id_lec):
                print("Eliminado.")
            else:
                print("No se pudo eliminar.")


def menu_pago(usuario_id: UUID) -> None:
    # Diccionario maestro de estados para que sea consistente en todo el menu
    estados_validos = {"1": "COMPLETADO", "2": "PENDIENTE", "3": "CANCELADO"}

    while True:
        print("\n--- Pagos ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opcion: ")
        if op == "0":
            return

        elif op == "1":
            pagos = service_pago.obtener_todos()
            if not pagos:
                print("No hay pagos registrados.")
            for p in pagos:
                print(
                    f"  {p.id_pago} | {p.monto} | {p.estado_pago} | Cliente: {p.id_usuario}"
                )

        elif op == "2":
            id_cliente = leer_uuid("ID del usuario que paga: ")
            if not id_cliente:
                print("El usuario es obligatorio.")
                continue

            monto = leer_float("Monto: ")
            if monto is None or monto <= 0:
                print("El monto debe ser mayor a 0.")
                continue    

            metodo = leer_texto("Metodo (Tarjeta/Efectivo): ")
            if not metodo:
                print("El método de pago es obligatorio.")
                continue

            id_curso = leer_uuid("ID del curso: ")
            if not id_curso:
                print("El ID del curso es obligatorio.")
                continue

            curso = services_curso.obtener_por_id(id_curso)
            if not curso:
                print("El curso no existe.")
                continue

            print("Seleccione el estado del pago:")
            print("1. COMPLETADO  2. PENDIENTE  3. CANCELADO")
            sel_estado = leer_texto("Opcion: ")

            if sel_estado not in estados_validos:
                print("Error: Selección de estado no válida.")
                continue

            estado_final = estados_validos[sel_estado]

            if estado_final == "COMPLETADO" and monto <= 0:
                print("Un pago completado debe tener monto mayor a 0.")
                continue

            try:
                service_pago.crear(
                    id_usuario_creacion=usuario_id,
                    id_usuario=id_cliente,
                    id_curso=id_curso,
                    monto=monto,
                    estado_pago=estado_final,
                    metodo_pago=metodo,
                )
                print(f"Pago registrado como: {estado_final}")

            except Exception as e:
                     print(f"Error al registrar: {e}")

        elif op == "3":
            id_pago = leer_uuid("ID pago a actualizar: ")
            if not id_pago:
                continue

            c = service_pago.obtener_por_id(id_pago)
            if not c:
                print("No existe ese registro.")
                continue

            monto_nuevo = leer_float(f"Nuevo monto (actual: {c.monto}): ") or c.monto

            print(f"Estado actual: {c.estado_pago}")
            print("Seleccione el nuevo estado (o Enter para mantener):")
            print("1. Completado  2. Pendiente  3. Cancelado")
            sel_estado = leer_texto("Opcion: ")

           
            if sel_estado == "":
                estado_final = c.estado_pago
            elif sel_estado in estados_validos:
                estado_final = estados_validos[sel_estado]
            else:
                print("Error: Seleccion no valida.")
                continue

            
            if monto_nuevo < 0:
                print("Error: El monto no puede ser negativo.")
                continue

            try:
                service_pago.actualizar(
                    id_pago=id_pago,
                    id_usuario_edita=usuario_id,
                    monto=monto_nuevo,
                    estado_pago=estado_final,
                )
                print(f"Pago actualizado con exito.")
            except Exception as e:
                print(f"Error: {e}")

        elif op == "4":
            id_pago = leer_uuid("ID pago a eliminar: ")
            if id_pago and service_pago.eliminar(id_pago):
                print("Eliminado.")
            else:
                print("No se pudo eliminar.")


def menu_evaluacion(usuario_id: UUID) -> None:
    while True:
        print("\n--- Evaluaciones ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opcion: ")
        if op == "0":
            return

        if op == "1":
            evaluaciones = service_evaluacion.obtener_todos()
            if not evaluaciones:
                print("No hay evaluaciones registradas.")
            for c in evaluaciones:
                print(
                    f"  {c.id_evaluacion} | {c.nombre_evaluacion} | {c.porcentaje}% | Leccion: {c.id_leccion}"
                )

        elif op == "2":
            nombre_evaluacion = leer_texto("Nombre de la evaluacion: ")
            porcentaje = leer_float("Porcentaje de la evaluacion (0-100): ")
            id_leccion = leer_uuid("ID de la leccion asociada: ")

            if not id_leccion or not service_leccion.obtener_por_id(id_leccion):
                print("Error: La leccion no existe o el ID es invalido.")
                continue

            if nombre_evaluacion and porcentaje > 0:
                try:

                    service_evaluacion.crear(
                        id_usuario_creacion=usuario_id,
                        id_leccion=id_leccion,
                        nombre_evaluacion=nombre_evaluacion,
                        porcentaje=porcentaje,
                    )
                    print("Evaluacion creada.")
                except Exception as e:
                    print(f"Error al crear evaluacion: {e}")
            else:
                print("El nombre y un porcentaje valido son obligatorios.")

        elif op == "3":
            id_eval = leer_uuid("ID evaluacion a actualizar: ")
            if not id_eval:
                continue

            c = service_evaluacion.obtener_por_id(id_eval)
            if not c:
                print("No existe esa evaluacion.")
                continue

            nombre = (
                leer_texto(f"Nuevo nombre (actual: {c.nombre_evaluacion}): ")
                or c.nombre_evaluacion
            )
            porc = (
                leer_float(f"Nuevo porcentaje (actual: {c.porcentaje}): ")
                or c.porcentaje
            )

            nuevo_id_lec = leer_uuid(f"Nuevo ID de leccion (actual: {c.id_leccion}): ")
            id_leccion_final = (
                nuevo_id_lec
                if nuevo_id_lec and service_leccion.obtener_por_id(nuevo_id_lec)
                else c.id_leccion
            )

            try:

                service_evaluacion.actualizar(
                    id_evaluacion=id_eval,
                    id_usuario_edita=usuario_id,
                    nombre_evaluacion=nombre,
                    porcentaje=porc,
                    id_leccion=id_leccion_final,
                )
                print("Actualizado.")
            except Exception as e:
                print(f"Error al actualizar: {e}")

        elif op == "4":
            id_eval = leer_uuid("ID evaluacion a eliminar: ")
            if id_eval and service_evaluacion.eliminar(id_eval):
                print("Eliminado.")
            else:
                print("No se pudo eliminar (ID inexistente o invalido).")


def menu_inscripciones(usuario_id: UUID) -> None:
    while True:
        print("\n--- Inscripciones ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            inscripciones = services_inscripcion.obtener_todos()

            if not inscripciones:
                print("No hay inscripciones registradas.")
                continue

            for i in inscripciones:
                print(
                    f"ID Inscripción: {i.id_inscripcion} | "
                    f"Curso: {i.id_curso} | "
                    f"Usuario inscrito: {i.id_usuario_inscrito} | "
                    f"Estado: {i.estado_inscripcion}"
                )

        elif op == "2":
            cursos = services_curso.obtener_todos()

            if not cursos:
                print("No hay cursos creados. Debes crear uno primero.")
                continue

            print("Cursos disponibles:")
            for curso in cursos:
                print(f"  {curso.id_curso} | {curso.nombre_curso}")
            id_curso = leer_uuid("ID curso: ")
            if not id_curso:
                print("ID curso inválido.")
                continue
            Usuarios_inscritos = services_usuario.obtener_todos()

            if not Usuarios_inscritos:
                print("No hay usuarios inscritos. Debes crear uno primero.")
                continue

            print("Usuarios disponibles:")
            for usuario in Usuarios_inscritos:
                print(
                    f"  {usuario.id_usuario} | {usuario.nombre_usuario} | {usuario.documento_identidad}"
                )

            id_usuario_incrito = leer_uuid("ID usuario a inscribir: ")
            if not id_usuario_incrito:
                print("ID usuario inválido.")
                continue

            try:
                inscripcion_creada = services_inscripcion.crear(
                    id_curso=id_curso,
                    id_usuario_inscrito=id_usuario_incrito,
                    id_usuario_creacion=usuario_id,
                )
                
            except Exception as e:
                print("Error al crear inscripción:", e)
                return None
        elif op == "3":
            id_inscripcion = leer_uuid("ID inscripción a actualizar: ")
            if not id_inscripcion:
                print("ID inválido.")
                continue
            c = services_inscripcion.obtener_por_id(id_inscripcion)
            if not c:
                print("No existe esa inscripción.")
                continue
            estado_inscripcion = (
                leer_texto(f"Nuevo estado (actual: {c.estado_inscripcion}): ")
                or c.estado_inscripcion
            )
            services_inscripcion.actualizar(
                id_inscripcion=id_inscripcion,
                usuario_id=usuario_id,
                estado_inscripcion=estado_inscripcion,
            )
            print("Actualizado.")
        elif op == "4":
            id_inscripcion = leer_uuid("ID inscripción a eliminar: ")
            try:
                if id_inscripcion and services_inscripcion.eliminar(id_inscripcion):
                    print("Eliminado.")
                else:
                    print("No se pudo eliminar (ID inválido o no existe).")
            except ValueError as e:
                print("Error:", e)
                
def menu_calificaciones(usuario_id: UUID) -> None:
    while True:
        print("\n--- Calificaciones ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            for c in services_calificacion.obtener_todos():
                print(
                    f"  {c.id_inscripcion} | {c.id_evaluacion} | {c.Nota}"
                )
        elif op == "2":
            id_inscripcion = leer_uuid("ID de la inscripción: ")
            id_evaluacion = leer_uuid("ID de la evaluación: ")
            nota = leer_float("Nota obtenida: ")

            if not services_inscripcion.obtener_por_id(id_inscripcion):
                print("La inscripción no existe o no es válida.")
                continue

            if not service_evaluacion.obtener_por_id(id_evaluacion):
                print("La evaluación no existe o no es válida.")
                continue

            if id_inscripcion and id_evaluacion and nota is not None:
                try:
                    services_calificacion.crear(
                        id_inscripcion=id_inscripcion,
                        id_evaluacion=id_evaluacion,
                        Nota=nota,
                        id_usuario_creacion=usuario_id,
                    )
                    print("Calificación creada.")
                except ValueError as e:
                    print("Error:", e)
            else:
                print("Todos los campos son obligatorios.")
        elif op == "3":
            id_inscripcion = leer_uuid(
                "ID inscripción de la calificación a actualizar: "
            )
            id_evaluacion = leer_uuid("ID evaluación de la calificación a actualizar: ")
            if not id_inscripcion or not id_evaluacion:
                print("IDs inválidos.")
                continue
            c = services_calificacion.obtener_por_id(id_inscripcion, id_evaluacion)
            if not c:
                print("No existe esa calificación.")
                continue
            Nota = leer_float(f"Nueva nota (actual: {c.Nota}): ") or c.Nota
            services_calificacion.actualizar(
                id_inscripcion, id_evaluacion, usuario_id, Nota=Nota
            )
            print("Actualizado.")
        elif op == "4":
            id_inscripcion = leer_uuid("ID inscripción de la calificación a eliminar: ")
            id_evaluacion = leer_uuid("ID evaluación de la calificación a eliminar: ")
            if (
                id_inscripcion
                and id_evaluacion
                and services_calificacion.eliminar(id_inscripcion, id_evaluacion)
            ):
                print("Eliminada.")
            else:
                print("No se pudo eliminar (IDs inválidos o no existe).")
        if op == "1":
            calificaciones = services_calificacion.obtener_todos()
            if not calificaciones:
                print("No hay calificaciones registradas.")
            else:
                for c in calificaciones:
                    print(f"  {c.id_inscripcion} | {c.id_evaluacion} | {c.Nota}")

def menu_certificados(usuario_id: UUID) -> None:
    while True:
        print("\n--- Certificados ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            certificados = services_certificado.obtener_todos()
            if not certificados:
                print("No hay certificados registrados.")
            else:
                for c in certificados:
                    print(f"  {c.id_certificado} | {c.id_inscripcion} | {c.fecha_creacion}")

        elif op == "2":
            id_inscripcion = leer_uuid("ID de la inscripción: ")
            
            if not services_inscripcion.obtener_por_id(id_inscripcion):
                print("La inscripción no existe o no es válida.")
                continue

            if id_inscripcion:
                try:
                    services_certificado.crear(
                        id_inscripcion=id_inscripcion, id_usuario_creacion=usuario_id
                    )
                    print("Certificado creado.")
                except Exception as e:
                    print("Error:", e)
            else:
                print("Todos los campos son obligatorios.")
        elif op == "3":
            id_cert = leer_uuid("ID certificado a actualizar: ")
            if not id_cert:
                print("ID inválido.")
                continue
            c = services_certificado.obtener_por_id(id_cert)
            if not c:
                print("No existe ese certificado.")
                continue
            nuevo_id_inscripcion = leer_uuid(
                f"Nuevo ID de inscripción (actual: {c.id_inscripcion}): "
            )

            if nuevo_id_inscripcion is None:
                id_inscripcion = c.id_inscripcion
            else:
                if not services_inscripcion.obtener_por_id(nuevo_id_inscripcion):
                    print("La inscripción no existe o no es válida.")
                    continue
                id_inscripcion = nuevo_id_inscripcion

            services_certificado.actualizar(
                id_cert,
                usuario_id,
                id_inscripcion=id_inscripcion,
            )
            print("Actualizado.")
        elif op == "4":
            id_cert = leer_uuid("ID certificado a eliminar: ")
            if id_cert and services_certificado.eliminar(id_cert):
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
        print(
            """
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
        """
        )

        op = leer_texto("Opción: ")
        if op == "0":
            print(f"Hasta luego {usuario.nombre_usuario}.")
            break
        if op == "1":
            menu_categorias(usuario.id_usuario)
            continue
        elif op == "2":
            menu_cursos(usuario.id_usuario)
            continue
        elif op == "3":
            menu_leccion(usuario.id_usuario)
            continue

        elif op == "4":
            menu_material(usuario.id_usuario)
            continue

        elif op == "5":
            menu_evaluacion(usuario.id_usuario)
            continue

        elif op == "6":
            menu_pago(usuario.id_usuario)
            continue

        elif op == "7":
            menu_inscripciones(usuario.id_usuario)
            continue

        elif op == "8":
            menu_calificaciones(usuario.id_usuario)
            continue
        elif op == "9":
            menu_certificados(usuario.id_usuario)
            continue


        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
