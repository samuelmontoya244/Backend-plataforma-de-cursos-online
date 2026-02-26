from src.entities.plataforma import Plataforma


# ==========================
# FUNCIONES DE VALIDACION
# ==========================


def validar_entero(valor: str, minimo: int = 1) -> bool:
    """
    Valida que el valor sea un numero entero.
    (Regla: solo numeros y mayor o igual al minimo)
    """
    valor = valor.strip()

    if not valor.isdigit():
        print("Error: debe ingresar solo numeros.")
        return False

    if int(valor) < minimo:
        print(f"Error: el numero debe ser mayor o igual a {minimo}.")
        return False

    return True


def validar_texto(texto: str) -> bool:
    """
    Valida que el texto contenga solo letras.
    (Regla: no se permiten numeros ni caracteres especiales)
    """
    texto = texto.strip()

    if not texto:
        print("Error: el campo no puede estar vacio.")
        return False

    if not texto.replace(" ", "").isalpha():
        print("Error: solo se permiten letras.")
        return False

    return True


def validar_flotante_rango(valor: str, minimo: float, maximo: float) -> bool:
    """
    Valida que el valor sea decimal y este en rango.
    (Regla: numero valido entre minimo y maximo)
    """
    try:
        numero = float(valor)
    except ValueError:
        print("Error: debe ingresar un numero valido.")
        return False

    if numero < minimo or numero > maximo:
        print(f"Error: el numero debe estar entre {minimo} y {maximo}.")
        return False

    return True


# ==========================
# MENU
# ==========================


def menu() -> None:
    print("\n--- PLATAFORMA DE CURSO ONLINE ---")
    print("1. Crear curso")
    print("2. Registrar instructor")
    print("3. Registrar estudiante")
    print("4. Inscribir estudiante en curso")
    print("5. Calificar estudiante")
    print("6. Emitir certificado")
    print("7. Salir")


CURSOS_POR_DEFECTO = {"1": "Idioma", "2": "Diseño", "3": "Programacion"}


# ==========================
# PROGRAMA PRINCIPAL
# ==========================


def manejar_plataforma() -> None:
    plataforma = Plataforma()

    while True:
        menu()
        opcion = input("Seleccione una opcion: ")

        # CREAR CURSO
        if opcion == "1":
            opcion_curso = input(
                "Seleccione tipo (1 Idioma, 2 Diseño, 3 Programacion): "
            )

            if opcion_curso not in CURSOS_POR_DEFECTO:
                print("Curso no valido.")
                continue

            instructor_id = input("ID del instructor: ")
            if not validar_entero(instructor_id):
                continue

            instructor = plataforma.obtener_instructor_por_id(int(instructor_id))

            if instructor is None:
                print("El instructor no existe.")
                continue

            codigo = input("Codigo del curso: ")
            if not validar_entero(codigo):
                continue

            categoria = input("Categoria del curso: ")
            if not validar_texto(categoria):
                continue

            duracion = input("Duracion en horas: ")
            if not validar_entero(duracion):
                continue

            plataforma.crear_curso(
                codigo=int(codigo),
                nombre=CURSOS_POR_DEFECTO[opcion_curso],
                categoria=categoria,
                duracionhoras=int(duracion),
                instructor=instructor,
            )

            print("Curso creado correctamente.")

        # REGISTRAR INSTRUCTOR
        elif opcion == "2":
            instructor_id = input("ID del instructor: ")
            if not validar_entero(instructor_id):
                continue

            if plataforma.obtener_instructor_por_id(int(instructor_id)):
                print("El instructor ya existe.")
                continue

            nombre = input("Nombre: ")
            if not validar_texto(nombre):
                continue

            apellido = input("Apellido: ")
            if not validar_texto(apellido):
                continue

            cedula = input("Cedula: ")
            if not validar_entero(cedula):
                continue

            telefono = input("Telefono: ")
            if not validar_entero(telefono):
                continue

            especialidad = input("Especialidad: ")
            if not validar_texto(especialidad):
                continue

            plataforma.crear_instructor(
                id_usuario=int(instructor_id),
                nombre=nombre,
                apellido=apellido,
                cedula=cedula,
                telefono=telefono,
                especialidad=especialidad,
            )

            print("Instructor registrado correctamente.")

        # REGISTRAR ESTUDIANTE
        elif opcion == "3":
            estudiante_id = input("ID del estudiante: ")
            if not validar_entero(estudiante_id):
                continue

            if plataforma.obtener_estudiante_por_id(int(estudiante_id)):
                print("El estudiante ya existe.")
                continue

            nombre = input("Nombre: ")
            if not validar_texto(nombre):
                continue

            apellido = input("Apellido: ")
            if not validar_texto(apellido):
                continue

            cedula = input("Cedula: ")
            if not validar_entero(cedula):
                continue

            telefono = input("Telefono: ")
            if not validar_entero(telefono):
                continue

            plataforma.crear_estudiante(
                id_usuario=int(estudiante_id),
                nombre=nombre,
                apellido=apellido,
                cedula=cedula,
                telefono=telefono,
            )

            print("Estudiante registrado correctamente.")

        # CALIFICAR
        elif opcion == "5":
            estudiante_id = input("ID del estudiante: ")
            curso_codigo = input("Codigo del curso: ")

            if not validar_entero(estudiante_id):
                continue

            if not validar_entero(curso_codigo):
                continue

            nota = input("Nota final (0.0 a 5.0): ")
            if not validar_flotante_rango(nota, 0.0, 5.0):
                continue

            estudiante = plataforma.obtener_estudiante_por_id(int(estudiante_id))
            curso = plataforma.obtener_curso_por_codigo(int(curso_codigo))

            if estudiante and curso:
                plataforma.calificar_estudiante(estudiante, curso, float(nota))
                print("Nota registrada correctamente.")
            else:
                print("Estudiante o curso no encontrado.")

        # CERTIFICADO
        elif opcion == "6":
            estudiante_id = input("ID del estudiante: ")
            curso_codigo = input("Codigo del curso: ")

            if not validar_entero(estudiante_id):
                continue

            if not validar_entero(curso_codigo):
                continue

            estudiante = plataforma.obtener_estudiante_por_id(int(estudiante_id))
            curso = plataforma.obtener_curso_por_codigo(int(curso_codigo))

            if estudiante and curso:
                certificado = plataforma.emitir_certificado(estudiante, curso)
                print(certificado)
            else:
                print("Estudiante o curso no encontrado.")

        elif opcion == "7":
            print("Saliendo del programa...")
            break

        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    manejar_plataforma()
