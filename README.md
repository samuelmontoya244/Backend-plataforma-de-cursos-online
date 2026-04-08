⚙️ Descripción del proyecto

Se desarrolló una API REST que permite manejar la lógica principal de una plataforma de cursos online. A través de esta API se pueden realizar operaciones como:

Registro e inicio de sesión de usuarios
Creación y gestión de cursos
Inscripción de usuarios en cursos
Consulta de información

La aplicación está diseñada siguiendo buenas prácticas de desarrollo backend, separando responsabilidades y permitiendo escalabilidad.

🔌 Ejecución del proyecto

Para ejecutar la aplicación localmente:

Clonar el repositorio:
git clone     https://github.com/samuelmontoya244/Backend-plataforma-de-cursos-online
cd   Plataforma de cursos online
Crear y activar un entorno virtual:
python -m venv venv
source venv/bin/activate   # En Linux/Mac
venv\Scripts\activate      # En Windows
Instalar dependencias:
pip install -r requirements.txt
Ejecutar el servidor con Uvicorn:
uvicorn main:app --reload
Acceder a la documentación automática:
http://127.0.0.1:8000/docs
📡 Uso de la API

La API permite interactuar mediante endpoints REST. Algunos ejemplos:

POST /users → Crear usuario
POST /login → Autenticación
GET /courses → Obtener cursos
POST /courses → Crear curso

(Ajusta estos endpoints según tu código real)

🧪 Pruebas

Se pueden realizar pruebas directamente desde:

Swagger UI (/docs)
Postman
Thunder Client
🎥 Video demostración

Puedes ver el funcionamiento del proyecto en el siguiente enlace:

https://correoitmedu-my.sharepoint.com/:v:/g/personal/nicolascano1136534_correo_itm_edu_co/IQB3PKLiuUMER5eOx90H4C8PARINfneU5SiiqkmeGnE_0ZM?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=08Nm6J

👨‍💻 Autores

Nicolas Cano Lara

Samuel Esteban Montoya Galeano

Duvan Ocampo Gamez

🏫 Institución

Instituto Tecnológico Metropolitano (ITM)

📌 Notas adicionales
El servidor utiliza Uvicorn como ASGI server para ejecutar la aplicación FastAPI.
La arquitectura está pensada para facilitar futuras integraciones con frontend.
