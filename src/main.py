from src.entities.plataforma import Plataforma

def mostrar_menu():
    print("\n" + "="*50)
    print("PLATAFORMA DE CURSOS ONLINE")
    print("="*50)
    print("1. Crear curso")
    print("2. Registrar instructor")
    print("3. Registrar estudiante")
    print("4. Inscribir estudiante en curso")
    print("5. Calificar estudiante")
    print("6. Emitir certificado")
    print("7. Salir")
    print("="*50)

def obtener_entero(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Error: Ingrese un número válido.")

def obtener_cedula():
    while True:
        try:
            cedula = int(input("Ingrese la cédula: "))
            if cedula <= 0:
                print("Error: La cédula debe ser un número positivo.")
                continue
            return cedula
        except ValueError:
            print("Error: La cédula debe contener solo números.")

def obtener_telefono():
    while True:
        try:
            telefono = int(input("Ingrese el teléfono: "))
            if telefono <= 0:
                print("Error: El teléfono debe ser un número positivo.")
                continue
            return telefono
        except ValueError:
            print("Error: El teléfono debe contener solo números.")

def crear_curso(plataforma):
    print("\n--- CREAR CURSO ---")
    codigo = input("Ingrese el código del curso: ").strip()
    
    if plataforma.existe_curso(codigo):
        print(f"Error: El curso con código '{codigo}' ya existe.")
        return
    
    nombre = input("Ingrese el nombre del curso: ").strip()
    descripcion = input("Ingrese la descripción del curso: ").strip()
    
    print("\nInstructores disponibles:")
    if not plataforma.instructores:
        print("No hay instructores registrados. Primero registre un instructor.")
        return
    
    for i, instructor in enumerate(plataforma.instructores, 1):
        print(f"{i}. {instructor.get_nombre()} (Cédula: {instructor.get_cedula()})")
    
    opcion = obtener_entero("Seleccione el instructor (número): ") - 1
    if opcion < 0 or opcion >= len(plataforma.instructores):
        print("Error: Instructor no válido.")
        return
    
    instructor = plataforma.instructores[opcion]
    try:
        plataforma.crear_curso(codigo, nombre, descripcion, instructor)
        print(f"✓ Curso '{nombre}' creado exitosamente.")
    except ValueError as e:
        print(f"Error: {e}")

def registrar_instructor(plataforma):
    print("\n--- REGISTRAR INSTRUCTOR ---")
    cedula = obtener_cedula()
    
    if plataforma.existe_instructor(cedula):
        print(f"Error: El instructor con cédula {cedula} ya existe.")
        return
    
    nombre = input("Ingrese el nombre del instructor: ").strip()
    email = input("Ingrese el email del instructor: ").strip()
    telefono = obtener_telefono()
    
    try:
        plataforma.crear_instructor(cedula, nombre, email, telefono)
        print(f"✓ Instructor '{nombre}' registrado exitosamente.")
    except ValueError as e:
        print(f"Error: {e}")

def registrar_estudiante(plataforma):
    print("\n--- REGISTRAR ESTUDIANTE ---")
    cedula = obtener_cedula()
    
    if plataforma.existe_estudiante(cedula):
        print(f"Error: El estudiante con cédula {cedula} ya existe.")
        return
    
    nombre = input("Ingrese el nombre del estudiante: ").strip()
    email = input("Ingrese el email del estudiante: ").strip()
    telefono = obtener_telefono()
    
    try:
        plataforma.crear_estudiante(cedula, nombre, email, telefono)
        print(f"✓ Estudiante '{nombre}' registrado exitosamente.")
    except ValueError as e:
        print(f"Error: {e}")

def inscribir_estudiante(plataforma):
    print("\n--- INSCRIBIR ESTUDIANTE EN CURSO ---")
    
    if not plataforma.cursos:
        print("Error: No hay cursos disponibles. Primero cree un curso.")
        return
    
    if not plataforma.estudiantes:
        print("Error: No hay estudiantes registrados. Primero registre un estudiante.")
        return
    
    print("\nEstudiantes disponibles:")
    for i, estudiante in enumerate(plataforma.estudiantes, 1):
        print(f"{i}. {estudiante.get_nombre()} (Cédula: {estudiante.get_cedula()})")
    
    opcion_est = obtener_entero("Seleccione el estudiante (número): ") - 1
    if opcion_est < 0 or opcion_est >= len(plataforma.estudiantes):
        print("Error: Estudiante no válido.")
        return
    
    estudiante = plataforma.estudiantes[opcion_est]
    
    print("\nCursos disponibles:")
    for i, curso in enumerate(plataforma.cursos, 1):
        print(f"{i}. {curso.get_nombre()} (Código: {curso.get_codigo()})")
    
    opcion_cur = obtener_entero("Seleccione el curso (número): ") - 1
    if opcion_cur < 0 or opcion_cur >= len(plataforma.cursos):
        print("Error: Curso no válido.")
        return
    
    curso = plataforma.cursos[opcion_cur]
    try:
        plataforma.inscribir_estudiante(estudiante, curso)
        print(f"✓ Estudiante '{estudiante.get_nombre()}' inscrito en '{curso.get_nombre()}' exitosamente.")
    except ValueError as e:
        print(f"Error: {e}")

def calificar_estudiante(plataforma):
    print("\n--- CALIFICAR ESTUDIANTE ---")
    
    if not plataforma.inscripciones:
        print("Error: No hay estudiantes inscritos en cursos.")
        return
    
    print("\nInscripciones disponibles:")
    for i, inscripcion in enumerate(plataforma.inscripciones, 1):
        print(f"{i}. {inscripcion.get_estudiante().get_nombre()} en {inscripcion.get_curso().get_nombre()}")
    
    opcion = obtener_entero("Seleccione la inscripción (número): ") - 1
    if opcion < 0 or opcion >= len(plataforma.inscripciones):
        print("Error: Inscripción no válida.")
        return
    
    inscripcion = plataforma.inscripciones[opcion]
    calificacion = obtener_entero("Ingrese la calificación (0-5): ")
    
    if calificacion < 0 or calificacion > 5:
        print("Error: La calificación debe estar entre 0 y 5.")
        return
    
    plataforma.calificar_estudiante(inscripcion, calificacion)
    print(f"✓ Estudiante calificado con {calificacion}.")

def emitir_certificado(plataforma):
    print("\n--- EMITIR CERTIFICADO ---")
    
    inscripciones_calificadas = [i for i in plataforma.inscripciones if i.get_nota_final() is not None]
    
    if not inscripciones_calificadas:
        print("Error: No hay estudiantes calificados para emitir certificados.")
        return
    
    print("\nEstudiantes calificados:")
    for i, inscripcion in enumerate(inscripciones_calificadas, 1):
        estado = "✓ Aprobado" if inscripcion.get_nota_final() >= 3.0 else "✗ No aprobado"
        print(f"{i}. {inscripcion.get_estudiante().get_nombre()} - {inscripcion.get_curso().get_nombre()} ({estado}) - Calificación: {inscripcion.get_nota_final()}")
    
    opcion = obtener_entero("Seleccione la inscripción (número): ") - 1
    if opcion < 0 or opcion >= len(inscripciones_calificadas):
        print("Error: Inscripción no válida.")
        return
    
    inscripcion = inscripciones_calificadas[opcion]
    
    if inscripcion.get_nota_final() < 3.0:
        print("Error: El estudiante no aprobó el curso (calificación < 3.0).")
        return
    
    if plataforma.emitir_certificado(inscripcion):
        print(f"✓ Certificado emitido para {inscripcion.get_estudiante().get_nombre()}.")
    else:
        print("Error: No se pudo emitir el certificado.")

def main():
    plataforma = Plataforma()
    
    while True:
        mostrar_menu()
        opcion = obtener_entero("Seleccione una opción: ")
        
        if opcion == 1:
            crear_curso(plataforma)
        elif opcion == 2:
            registrar_instructor(plataforma)
        elif opcion == 3:
            registrar_estudiante(plataforma)
        elif opcion == 4:
            inscribir_estudiante(plataforma)
        elif opcion == 5:
            calificar_estudiante(plataforma)
        elif opcion == 6:
            emitir_certificado(plataforma)
        elif opcion == 7:
            print("\n¡Hasta luego!")
            break
        else:
            print("Error: Opción no válida. Ingrese un número del 1 al 7.")

if __name__ == "__main__":
    main()
