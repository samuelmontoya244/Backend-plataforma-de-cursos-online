
import sys
from typing import Optional
from uuid import UUID

sys.path.insert(0, ".")

from src.services import evaluacion as service_evaluacion
from src.services import leccion as service_leccion
from src.services import material as service_material
from src.services import pago as service_pago



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
    

def menu_material(usuario_id: UUID) -> None:
    while True:
        print("\n--- Materiales ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            for c in service_material.obtener_todos():
                print(f"  {c.id_material} | {c.titulo_material} | {c.tipo_material} | {c.URL_archivo} | {c.id_leccion}" )
        elif op == "2":
            titulo_material = leer_texto("Nombre material: ")
            tipo_material = leer_texto("Tipo de material: ")
            URL_archivo = leer_texto("URL del archivo: ")
            id_leccion = leer_uuid("ID de la lección: ")

            if not service_leccion.obtener_por_id(id_leccion):
                print("La lección no existe o no es valida.")
                continue

            if titulo_material and id_leccion and URL_archivo:
                try:
                    service_material.crear(usuario_id, id_leccion, titulo_material, tipo_material, URL_archivo)
                    print("Material creado.")
                except Exception as e:
                    print("Error:", e)
            else:
                print("Todos los campos son obligatorios.")
        elif op == "3":
            id_mat = leer_uuid("ID material a actualizar: ")
            if not id_mat:
                print("ID inválido.")
                continue
            c = service_material.obtener_por_id(id_mat)
            if not c:
                print("No existe ese material.")
                continue
            titulo_material = leer_texto(f"Nuevo título (actual: {c.titulo_material}): ") or c.titulo_material
            tipo_material = leer_texto(f"Nuevo tipo (actual: {c.tipo_material}): ") or c.tipo_material
            URL_archivo = leer_texto(f"Nueva URL (actual: {c.URL_archivo}): ") or c.URL_archivo
            nuevo_id_leccion= leer_uuid(f"Nuevo ID de lección (actual: {c.id_leccion}): ")

            if nuevo_id_leccion is None:
                id_leccion = c.id_leccion
            
            else:
                if not service_leccion.obtener_por_id(id_leccion):
                    print("La lección no existe o no es valida.")
                    continue
                id_leccion = nuevo_id_leccion

               

            service_material.actualizar(
                id_mat,
                usuario_id,
                titulo_material=titulo_material,
                tipo_material=tipo_material,
                URL_archivo=URL_archivo,
                id_leccion=id_leccion
            )
            print("Actualizado.")
        elif op == "4":
            id_mat = leer_uuid("ID material a eliminar: ")
            if id_mat and service_material.eliminar(id_mat):
                print("Eliminado.")
            else:
                print("No se pudo eliminar (ID inválido o no existe).")

def menu_leccion(usuario_id: UUID) -> None:
    while True:
        print("\n--- Lecciones ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            for c in service_leccion.obtener_todos():
                print(f"  {c.id_leccion} | {c.titulo_leccion} | {c.descripcion_leccion} | {c.orden} | {c.duracion_horas} | {c.id_curso}" )
        elif op == "2":
            titulo_leccion = leer_texto("Nombre de la lección: ")
            descripcion_leccion = leer_texto("Descripción de la lección: ")
            orden = leer_int("Orden de la lección: ")
            duracion_horas = leer_float("Duración en horas: ")
            id_curso = leer_uuid("ID del curso: ")



            if not service_curso.obtener_por_id(id_curso):
                print("El curso no existe o no es válido.")
                continue
            
            if service_leccion.obtener_por_orden_y_curso(orden, id_curso):
                print("Ya existe una lección con ese orden en ese curso.")
                continue

            if titulo_leccion and descripcion_leccion and orden and duracion_horas and id_curso:
                try:
                    service_leccion.crear(usuario_id, titulo_leccion, descripcion_leccion, orden, duracion_horas, id_curso)
                    print("Lección creada.")
                except Exception as e:
                    print("Error:", e)
            else:
                print("Todos los campos son obligatorios.")
        elif op == "3":
            id_lec = leer_uuid("ID lección a actualizar: ")
            if not id_lec:
                print("ID inválido.")
                continue
            c = service_leccion.obtener_por_id(id_lec)
            if not c:
                print("No existe esa lección.")
                continue
            titulo_leccion = leer_texto(f"Nuevo título (actual: {c.titulo_leccion}): ") or c.titulo_leccion
            descripcion_leccion = leer_texto(f"Nueva descripción (actual: {c.descripcion_leccion}): ") or c.descripcion_leccion
            nuevo_orden = leer_int(f"Nuevo orden (actual: {c.orden}): ")
            nuevo_id_curso= leer_uuid(f"Nuevo ID de curso (actual: {c.id_curso}): ")
            duracion_horas = leer_float(f"Nueva duración en horas (actual: {c.duracion_horas}): ") or c.duracion_horas

            if nuevo_orden == 0:
                orden = c.orden
            
            else:
                if (
                    service_leccion.obtener_por_orden_y_curso(nuevo_orden, c.id_curso)
                    and nuevo_orden != c.orden
                    
                    ):
                    print("Ya existe una lección con ese orden en ese curso.")
                    continue
                orden = nuevo_orden
            
            

            if nuevo_id_curso is None:
                id_curso = c.id_curso
            
            else:
                if not service_curso.obtener_por_id(nuevo_id_curso):
                    print("El curso no existe o no es válido.")
                    continue
                id_curso = nuevo_id_curso

               

            service_leccion.actualizar(
                id_lec,
                usuario_id,
                titulo_leccion=titulo_leccion,
                descripcion_leccion=descripcion_leccion,
                orden=orden,
                duracion_horas=duracion_horas,
                id_curso=id_curso
            )
            print("Actualizado.")
        elif op == "4":
            id_lec = leer_uuid("ID lección a eliminar: ")
            if id_lec and service_leccion.eliminar(id_lec):
                print("Eliminado.")
            else:
                print("No se pudo eliminar (ID inválido o no existe).")

def menu_evaluacion(usuario_id: UUID) -> None:
    while True:
        print("\n--- Evaluaciones ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            for c in service_evaluacion.obtener_todos():
                print(f"  {c.id_evaluacion} | {c.titulo_evaluacion} | {c.descripcion_evaluacion} | {c.puntos_maximos} | {c.id_leccion}" )
        elif op == "2":
            nombre_evaluacion = leer_texto("Nombre de la evaluación: ")
            porcentaje = leer_float("Porcentaje de la evaluacion: ")
            id_leccion = leer_uuid("ID de la lección: ")

            if not service_leccion.obtener_por_id(id_leccion):
                print("La lección no existe o no es valida.")
                continue

            if nombre_evaluacion and id_leccion and porcentaje:
                try:
                    service_evaluacion.crear(usuario_id, id_leccion, nombre_evaluacion, descripcion_evaluacion, puntos_maximos)
                    print("Evaluación creada.")
                except Exception as e:
                    print("Error:", e)
            else:
                print("Todos los campos son obligatorios.")
        elif op == "3":
            id_eval = leer_uuid("ID evaluacion a actualizar: ")
            if not id_eval:
                print("ID inválido.")
                continue
            c = service_evaluacion.obtener_por_id(id_eval)
            if not c:
                print("No existe esa evaluación.")
                continue
            nombre_evaluacion = leer_texto(f"Nuevo nombre (actual: {c.nombre_evaluacion}): ") or c.nombre_evaluacion
            porcentaje = leer_float(f"Nuevo porcentaje (actual: {c.porcentaje}): ") or c.porcentaje
            nuevo_id_leccion= leer_uuid(f"Nuevo ID de lección (actual: {c.id_leccion}): ")
            
            if nuevo_id_leccion is None:
                id_leccion = c.id_leccion
            
            else:
                if not service_leccion.obtener_por_id(id_leccion):
                    print("La lección no existe o no es valida.")
                    continue
                id_leccion = nuevo_id_leccion

               

            service_evaluacion.actualizar(
                id_eval,
                usuario_id,
                nombre_evaluacion=nombre_evaluacion,
                porcentaje=porcentaje,
                id_leccion=id_leccion
            )
            print("Actualizado.")
        elif op == "4":
            id_eval = leer_uuid("ID evaluación a eliminar: ")
            if id_eval and service_evaluacion.eliminar(id_eval):
                print("Eliminado.")
            else:
                print("No se pudo eliminar (ID inválido o no existe).")


def menu_pago(usuario_id: UUID) -> None:
    while True:
        print("\n--- Pagos ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            for c in service_pago.obtener_todos():
                print(f"  {c.id_pago} | {c.id_usuario} | {c.monto} | {c.estado_pago} | {c.metodo_pago}" )
        elif op == "2":
            id_usuario   = leer_uuid("ID del usuario a pagar: ")
            monto = leer_float("Monto del pago: ")
            estado_pago = leer_texto("Estado del pago: ")
            metodo_pago = leer_texto("Método de pago: ")
            id_curso = leer_uuid("ID del curso que va ha pagar: ")

            if not service_usuario.obtener_por_id(id_usuario):
                print("El usuario no existe o no es válido.")
                continue

            if not service_curso.obtener_por_id(id_curso):
                print("El curso no existe o no es válido.")
                continue

            if id_usuario and monto and estado_pago and metodo_pago and id_curso:
                try:
                    service_pago.crear(id_usuario, monto, estado_pago, metodo_pago, id_curso)
                    print("Pago creado.")
                except Exception as e:
                    print("Error:", e)
            else:
                print("Todos los campos son obligatorios.")
        elif op == "3":
            id_pago = leer_uuid("ID pago a actualizar: ")
            if not id_pago:
                print("ID inválido.")
                continue
            c = service_pago.obtener_por_id(id_pago)
            if not c:
                print("No existe ese pago.")
                continue
            nuevo_id_usuario= leer_uuid(f"Nuevo ID de usuario (actual: {c.id_usuario}): ")
            monto = leer_float(f"Nuevo monto (actual: {c.monto}): ") or c.monto
            estado_pago = leer_texto(f"Nuevo estado de pago (actual: {c.estado_pago}): ") or c.estado_pago
            metodo_pago = leer_texto(f"Nuevo método de pago (actual: {c.metodo_pago}): ") or c.metodo_pago
            nuevo_id_curso= leer_uuid(f"Nuevo ID de curso (actual: {c.id_curso}): ")

            if nuevo_id_curso is None:
                id_curso = c.id_curso
            
            else:
                if not service_curso.obtener_por_id(id_curso):
                    print("El curso no existe o no es válido.")
                    continue
                id_curso = nuevo_id_curso

            if nuevo_id_usuario is None:
                id_usuario = c.id_usuario
            
            else:
                if not service_usuario.obtener_por_id(id_usuario):
                    print("El usuario no existe o no es válido.")
                    continue
                id_usuario = nuevo_id_usuario

               

            service_pago.actualizar(
                id_pago,
                id_usuario=id_usuario,
                monto=monto,
                estado_pago=estado_pago,
                metodo_pago=metodo_pago,
                id_curso=id_curso
            )
                
    
            print("Actualizado.")
        elif op == "4":
            id_pago = leer_uuid("ID pago a eliminar: ")
            if id_pago and service_pago.eliminar(id_pago):
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
        print("1. Pagos  2. Materiales  3. Lecciones 4. Evaluaciones 0. Salir")
        op = leer_texto("Opción: ")
        if op == "0":
            print(f"Hasta luego {usuario.nombre_usuario}.")
            break
        if op == "1":
            menu_pago(usuario.id_usuario)
        elif op == "2":
            menu_material(usuario.id_usuario)
        elif op == "3":
            menu_leccion(usuario.id_usuario)
        
        elif op == "4":
            menu_evaluacion(usuario.id_usuario)
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()