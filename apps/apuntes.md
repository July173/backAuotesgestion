# flujo del sitemas de como debe de ir las partes para crear un endpoint

    Lo que describes es básicamente un flujo de arquitectura por capas para desarrollar un endpoint, donde cada parte tiene una responsabilidad muy clara y se conecta con la siguiente, manteniendo el código organizado, escalable y fácil de mantener.

    Te lo desgloso en orden de ejecución y responsabilidad:

## Flujo

BD <--> Model <--> DTO (Serializer) <--> Data (Repository) <--> Business (Services) <--> Controller (View)

    BD (Base de Datos)

        Es el almacenamiento físico de la información.
        Aquí están las tablas, relaciones, índices, etc.

    Model (Modelo de la Entidad)

        Representa una tabla o entidad de la BD en el código.
        Define los atributos (columnas) y sus tipos de datos.
        Ejemplo en C#: una clase Usuario con propiedades Id, Nombre, Email.

    DTO / Serializer (Data Transfer Object)

        Objeto intermedio que define qué datos se envían o reciben desde el frontend/API.
        Sirve para proteger la base de datos (no exponer todos los campos) y controlar el formato de entrada/salida.
        Ejemplo: UsuarioDTO que solo devuelve Nombre y Email, no la contraseña.

    Data / Repository (Acceso a Datos)

        Capa que consulta y escribe en la base de datos usando los modelos.
        Encapsula la lógica de acceso a datos para que el resto del sistema no dependa de la BD directamente.
        Ejemplo: UsuarioRepository.GetById(id) que retorna un usuario.
        
        👉 **Uso de métodos base:**
        Los repositorios heredan de `BaseRepository` y pueden usar métodos como:
        - `get_all()` para obtener todos los registros
        - `get_by_id(id)` para obtener uno por id
        - `create(data)` para crear un registro
        - `update(entity)` para actualizar
        - `delete(id)` para eliminar
        - `soft_delete(id)` para borrado lógico
        
        Puedes extender el repositorio con métodos personalizados si lo necesitas, pero la mayoría de operaciones CRUD ya están cubiertas por los métodos base del core.

    Business / Services (Lógica de Negocio)

        Aquí está la lógica del sistema (reglas, validaciones, procesos).
        Usa el repositorio para traer datos y aplicar la lógica antes de devolverlos.
        Ejemplo: UsuarioService.CrearUsuario(dto) que valida si el email ya existe antes de guardar.
        
        👉 **Uso de métodos base:**
        Los servicios heredan de `BaseService` y pueden usar métodos como:
        - `list()` para listar todos
        - `get(id)` para obtener uno
        - `create(data)` para crear
        - `update(id, data)` para actualizar
        - `partial_update(id, data)` para actualizar parcialmente
        - `delete(id)` para eliminar
        - `soft_delete(id)` para borrado lógico
        
        Puedes extender el service con lógica de negocio específica, pero las operaciones CRUD básicas ya están cubiertas por los métodos base del core.

    Controller / View (Controlador / Endpoint)

        Recibe las peticiones HTTP (GET, POST, PUT, DELETE).
        Llama a la capa de negocio y devuelve la respuesta formateada (JSON, HTML, etc.).
        Ejemplo: POST /usuarios que recibe un JSON, llama a UsuarioService y responde con el DTO creado.
        
        👉 **Uso de métodos base:**
        Los controladores heredan de `BaseViewSet` y pueden usar métodos como:
        - `list(request)` para GET todos
        - `retrieve(request, pk)` para GET uno
        - `create(request)` para POST
        - `update(request, pk)` para PUT
        - `partial_update(request, pk)` para PATCH
        - `destroy(request, pk)` para DELETE
        - `soft_destroy(request, pk)` para borrado lógico
        
        Puedes agregar acciones personalizadas usando `@action` si necesitas lógica especial.

📌 Resumen mental:

    BD → almacena
    Model → representa
    DTO → transforma datos de entrada/salida
    Repository → consulta/guarda datos (usando métodos base)
    Service → aplica lógica (usando métodos base)
    Controller → expone la API (usando métodos base)
