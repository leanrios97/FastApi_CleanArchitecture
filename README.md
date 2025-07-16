# API de Tareas con Arquitectura Limpia

Un proyecto simple en FastAPI que implementa Arquitectura Limpia, principios SOLID y patrones de diseño.

## Configuración

1. Crea un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecuta la aplicación:

```bash
uvicorn src.main:app --reload
```

## Configuración de la Base de Datos

El proyecto utiliza SQLite como base de datos y SQLAlchemy como ORM. La base de datos se configura automáticamente al iniciar la aplicación.

- **Archivo de la base de datos**: Se crea un archivo `todos.db` en el directorio raíz del proyecto cuando se ejecuta la aplicación por primera vez.
- **Inicialización**: Las tablas de la base de datos se crean automáticamente gracias al código en `src/main.py`, que usa `Base.metadata.create_all(bind=engine)`.
- **Ubicación**: La configuración de la base de datos está definida en `src/config.py` con la URL `sqlite:///./todos.db`.
- **Gestión**: No se requieren pasos adicionales para configurar la base de datos. SQLite no necesita un servidor dedicado, y el archivo de la base de datos es portátil.

### Inspección de la Base de Datos

Si necesitas inspeccionar o consultar la base de datos:

- Usa herramientas como `DB Browser for SQLite` o `sqlite3` desde la línea de comandos para abrir y consultar el archivo `todos.db`.
- Ejemplo con `sqlite3`:

  ```bash
  sqlite3 todos.db
  .tables
  SELECT * FROM todos;
  ```

### Nota sobre SQLite

SQLite tiene limitaciones en entornos multi-hilo, ya que los objetos de conexión solo pueden usarse en el hilo donde se crearon. Para evitar errores como `SQLite objects created in a thread can only be used in that same thread`, el proyecto configura el motor de SQLAlchemy con `connect_args={"check_same_thread": False}` en `src/infrastructure/database/database.py`. Sin embargo:

- Esta configuración es adecuada solo para entornos de desarrollo o aplicaciones con baja concurrencia.
- Para producción, considera usar una base de datos como PostgreSQL o MySQL, que manejan mejor la concurrencia y los entornos multi-hilo.

### 

## Arquitectura del Proyecto

El proyecto sigue los principios de **Arquitectura Limpia (Clean Architecture)**, organizando el código en capas claramente definidas para lograr una separación de responsabilidades, mantenibilidad y escalabilidad. Las capas son:

- **Capa de Dominio (Domain Layer)**:

  - Contiene la lógica de negocio central del proyecto.
  - Incluye las entidades (`Todo`), interfaces de repositorios (`TodoRepository`) y casos de uso (`CreateTodoUseCase`, `GetTodoUseCase`, `ListTodosUseCase`, `UpdateTodoUseCase`, `DeleteTodoUseCase`).
  - Es independiente de cualquier tecnología o framework, lo que permite que la lógica de negocio sea reutilizable y testable.
  - Ubicación: `src/domain/`.

- **Capa de Infraestructura (Infrastructure Layer)**:

  - Implementa los detalles técnicos, como la interacción con la base de datos.
  - Incluye la configuración de SQLAlchemy (`database.py`), los modelos de datos (`TodoModel`) y la implementación concreta del repositorio (`SQLTodoRepository`).
  - Se encarga de traducir las operaciones de la capa de dominio a operaciones específicas de la base de datos (SQLite en este caso).
  - Ubicación: `src/infrastructure/`.

- **Capa de Presentación (Presentation Layer)**:

  - Maneja la interacción con el mundo exterior, como las solicitudes HTTP y las respuestas.
  - Incluye el controlador de FastAPI (`todo_controller.py`) y las dependencias (`dependencies.py`) que conectan la lógica de negocio con la API.
  - Transforma los datos de entrada/salida entre el formato de la API y las entidades de dominio.
  - Ubicación: `src/presentation/`.

Esta estructura asegura que las dependencias fluyan hacia adentro (de la presentación al dominio), respetando el principio de inversión de dependencias y facilitando la sustitución de componentes (por ejemplo, cambiar SQLite por PostgreSQL).

## Patrones de Diseño y Principios SOLID

El proyecto implementa varios patrones de diseño y sigue los principios SOLID para garantizar un código robusto, mantenible y escalable.

### Patrones de Diseño

- **Patrón Repositorio**:

  - Se utiliza para abstraer el acceso a los datos, definiendo una interfaz (`TodoRepository`) en la capa de dominio que es implementada por `SQLTodoRepository` en la capa de infraestructura.
  - Permite cambiar la implementación de la base de datos sin afectar la lógica de negocio.
  - Ejemplo: `src/domain/repositories/todo_repository.py` y `src/infrastructure/repositories/sql_todo_repository.py`.

- **Patrón de Caso de Uso (Use Case Pattern)**:

  - Encapsula la lógica de negocio en clases dedicadas (`CreateTodoUseCase`, `GetTodoUseCase`, etc.), cada una responsable de una operación específica.
  - Facilita la reutilización y el testeo de la lógica de negocio.
  - Ejemplo: `src/domain/use_cases/`.

- **Inyección de Dependencias**:

  - Se utiliza el sistema de inyección de dependencias de FastAPI (`Depends`) para proporcionar instancias de repositorios a los casos de uso y controladores.
  - Esto asegura que las dependencias sean configurables y fáciles de reemplazar.
  - Ejemplo: `src/presentation/dependencies.py` y el uso de `Depends(get_todo_repository)` en `todo_controller.py`.

### Principios SOLID

- **S (Single Responsibility Principle - Principio de Responsabilidad Única)**:

  - Cada clase tiene una única responsabilidad. Por ejemplo, `CreateTodoUseCase` solo se encarga de crear tareas, `SQLTodoRepository` solo maneja operaciones de base de datos, y `todo_controller.py` solo gestiona las solicitudes HTTP.
  - Esto reduce el acoplamiento y facilita el mantenimiento.

- **O (Open/Closed Principle - Principio Abierto/Cerrado)**:

  - Las clases están abiertas para extensión pero cerradas para modificación. Por ejemplo, se pueden añadir nuevos casos de uso (como `DeleteTodoUseCase`) sin modificar el código existente de otros casos de uso o controladores.
  - La interfaz `TodoRepository` permite extender el sistema con nuevas implementaciones de repositorios.

- **L (Liskov Substitution Principle - Principio de Sustitución de Liskov)**:

  - Cualquier implementación de `TodoRepository` (como `SQLTodoRepository`) puede sustituirse sin afectar el comportamiento del sistema, ya que todas cumplen con el contrato definido en la interfaz.
  - Esto permite cambiar la base de datos (por ejemplo, a PostgreSQL) sin modificar los casos de uso.

- **I (Interface Segregation Principle - Principio de Segregación de Interfaz)**:

  - La interfaz `TodoRepository` define solo los métodos necesarios para la gestión de tareas (`create`, `get_by_id`, `list_all`, `update`, `delete`), evitando métodos innecesarios.
  - Esto asegura que las implementaciones no se vean obligadas a implementar funcionalidades no requeridas.

- **D (Dependency Inversion Principle - Principio de Inversión de Dependencias)**:

  - Los casos de uso dependen de la interfaz `TodoRepository` (abstracción) en lugar de una implementación concreta (`SQLTodoRepository`).
  - Las dependencias se inyectan a través de `Depends` en FastAPI, lo que facilita la sustitución de componentes.

```
todo_app/
├── src/
│   ├── domain/
│   │   ├── entities/
│   │   │   └── todo.py
│   │   ├── repositories/
│   │   │   └── todo_repository.py
│   │   └── use_cases/
│   │       ├── create_todo.py
│   │       ├── get_todo.py
│   │       ├── list_todos.py
│   │       ├── update_todo.py
│   │       └── delete_todo.py
│   ├── infrastructure/
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── database.py
│   │   │   └── models/
│   │   │       └── todo_model.py
│   │   └── repositories/
│   │       └── sql_todo_repository.py
│   ├── presentation/
│   │   ├── api/
│   │   │   └── todo_controller.py
│   │   └── dependencies.py
|   ├── logs/
│   ├── main.py
│   └── config
|
|── tests/
    |── test_todo_controller.py
    └── test_todo_use_cases.py
```


## Endpoints de la API

- POST /todos: Crear una nueva tarea.
- GET /todos/{id}: Obtener una tarea por ID.
- GET /todos: Listar todas las tareas.
- PUT /todos: Actualizar una tarea.
- DELETE /todos/{id}: Eliminar una tarea por ID.

## Pruebas

Ejecuta las pruebas con:

```bash
pytest tests/
```
