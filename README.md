# Backend – Plataforma de Cursos Online

Proyecto backend desarrollado en **Python**, orientado a objetos, que simula el funcionamiento de una **plataforma de cursos online**, permitiendo la gestión de usuarios, cursos e inscripciones.

---

## 📌 Características

* Gestión de **usuarios** (estudiantes e instructores)
* Creación y administración de **cursos**
* Inscripción de estudiantes a cursos
* Arquitectura modular
* Código alineado con la **guía de estilo PEP 8**

---

## 📂 Estructura del Proyecto

```
Backend-plataforma-de-cursos-online/
│
├── src/
│   ├── main.py
│   └── entities/
│       ├── usuario.py
│       ├── estudiante.py
│       ├── instructor.py
│       ├── curso.py
│       ├── inscripciones.py
│       ├── plataforma.py
│       └── __init__.py
│
├── .gitignore
└── README.md
```

---

## ⚙️ Requisitos

* Python **3.9** o superior
* No requiere librerías externas

---

## ▶️ Ejecución

Desde la raíz del proyecto, ejecutar:

```bash
python src/main.py
```

---

## 🧱 Descripción de Módulos

* **usuario.py**: Clase base para los tipos de usuario.
* **estudiante.py**: Manejo de estudiantes y sus cursos inscritos.
* **instructor.py**: Gestión de instructores.
* **curso.py**: Definición y atributos de los cursos.
* **inscripciones.py**: Lógica de inscripción.
* **plataforma.py**: Clase principal que coordina la aplicación.
* **main.py**: Punto de entrada del programa.

---

## 🧹 Estándar de Código – PEP 8

El proyecto sigue las recomendaciones de **PEP 8**:

* Nombres de variables y funciones en `snake_case`
* Clases en `CamelCase`
* Máximo **79 caracteres por línea**
* Uso de **docstrings** para clases y métodos
* Importaciones organizadas y claras
* Indentación de **4 espacios**

Ejemplo:

```python
class Estudiante(Usuario):
    """Representa un estudiante de la plataforma."""

    def inscribirse(self, curso):
        """Inscribe al estudiante en un curso."""
        self.cursos.append(curso)
```

---

## 🧪 Buenas Prácticas Aplicadas

* Programación orientada a objetos
* Separación de responsabilidades
* Código legible y mantenible
* Evita uso innecesario de `try/except`

---

## ✍️ Autores

* **Nicolas Cano Lara**
* **Samuel Esteban Montoya Galeano**

Institución: **ITM**

---

## 📄 Licencia

Proyecto académico con fines educativos.
