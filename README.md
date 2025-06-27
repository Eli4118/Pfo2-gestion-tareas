# Sistema de Gestión de Tareas (PFO2)

## Descripción
Sistema de gestión de tareas desarrollado como parte de la Práctica Formativa 2 (PFO2). Incluye una API REST con autenticación segura, base de datos SQLite e interfaz web para gestionar usuarios y tareas.

## Características
- ✅ Registro de usuarios con contraseñas hasheadas
- ✅ Autenticación mediante sesiones
- ✅ CRUD completo de tareas (Crear, Leer, Actualizar, Eliminar)
- ✅ Interfaz web responsive con Bootstrap
- ✅ API REST documentada
- ✅ Persistencia de datos con SQLite

## Requisitos Previos
- Python 3.7 o superior
- Pip (gestor de paquetes de Python)
- Navegador web moderno (Chrome, Firefox, Edge)

## Instalación y Ejecución

1. Clonar el repositorio  
   ```bash
   git clone https://github.com/Eli4i18/PFO2-gestion-tareas.git
   cd PFO2-gestion-tareas
   ```
2. Instalar dependencias  
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar la aplicación  
   ```bash
   python app.py
   ```
4. Acceder a la aplicación  
   Abre tu navegador y visita:  
   `http://localhost:5000`

## Uso de la Aplicación

- **Registro de nuevo usuario**  
  1. Accede a `http://localhost:5000/login_page`  
  2. Haz clic en "Regístrate aquí"  
  3. Completa el formulario  
- **Inicio de sesión**  
  Ingresa tus credenciales en el formulario de login  
- **Gestión de tareas**  
  - **Crear**: Ingresa descripción y haz clic en "Agregar Tarea"  
  - **Editar**: Haz clic en "Editar", modifica y guarda  
  - **Estado**: Usa "Marcar Completada/Pendiente" para cambiar estado  
  - **Eliminar**: Haz clic en "Eliminar" para borrar tareas

## Documentación de la API

### Registro de usuario
```
POST /registro
Content-Type: application/json

{
  "usuario": "nombre_usuario",
  "contraseña": "mi_contraseña"
}
```

### Inicio de sesión
```
POST /login
Content-Type: application/json

{
  "usuario": "nombre_usuario",
  "contraseña": "mi_contraseña"
}
```
## Gestión de tareas

Método	Endpoint	         Acción
GET	    /api/tareas	       Listar todas las tareas
POST	  /api/tareas	       Crear nueva tarea
GET	    /api/tareas/<id>	 Obtener tarea específica
PUT	    /api/tareas/<id>	 Actualizar tarea
DELETE	/api/tareas/<id>	 Eliminar tarea

## Estructura del Proyecto

```
PFO2-gestion-tareas/
├── app.py                 # Servidor principal (Flask)
├── requirements.txt       # Lista de dependencias
├── img                    # Imagenes de pruebas
├── tareas.db              # Base de datos SQLite (se crea automáticamente)
└── templates/             # Plantillas HTML
    ├── base.html          # Plantilla base para todas las páginas
    ├── index.html         # Página principal después de login
    ├── login.html         # Página de login/registro
    └── tareas.html        # Interfaz de gestión de tareas
```

## Respuestas Conceptuales

### ¿Por qué hashear contraseñas?
El hasheo de contraseñas es esencial por las siguientes razones:

- **Protección contra brechas de seguridad:** Si la base de datos se compromete, los atacantes no podrán obtener las contraseñas en texto plano.  
- **Irreversibilidad:** Un hash bien implementado no puede revertirse a la contraseña original.  
- **Verificación segura:** Permite comprobar credenciales sin almacenar el dato real.  
- **Cumplimiento de estándares:** Satisface prácticas básicas de seguridad y protección de datos.  

### Ventajas de usar SQLite en este proyecto
- **Sin configuración:** No requiere un servidor de base de datos separado.  
- **Portabilidad:** Toda la base de datos está contenida en un solo archivo (`tareas.db`).  
- **Ligereza:** Consume pocos recursos, ideal para aplicaciones pequeñas.  
- **Compatibilidad:** Soporte nativo en Python.  
- **Bajo mantenimiento:** Perfecto para proyectos académicos o carga moderada.  
- **Desarrollo ágil:** Permite iteraciones rápidas durante el desarrollo.  

## Tecnologías Utilizadas

**Backend:**
- Python 3  
- Flask  
- SQLite  
- Werkzeug  

**Frontend:**
- HTML5  
- CSS3 (Bootstrap 5)  
- JavaScript  

**Herramientas:**
- Git  
- Thunder Client  
- VS Code  

