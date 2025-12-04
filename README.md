# Back-end Proyecto Autogestión SENA

Pasos:
  1) pip install -r requirements.txt
  2) Configura variables de entorno MySQL o edita core/settings.py
  3) python manage.py makemigrations
  4) python manage.py migrate
  5) Actualizar la base de datos con el sql que esta predispuesto en la raiz del proyecto como sql.sql
  6) python manage.py createsuperuser
  7) daphne -b 0.0.0.0 -p 8000 core.asgi:application
  8) celery -A core worker --loglevel=info
  9) celery -A core beat --loglevel=info  

  10) url del navegador : http://127.0.0.1:8000/swagger/

# Comandos esenciales para levantar el contenedor y correr migraciones

```bash
# Levantar todos los servicios
docker-compose up --build

# Generar migraciones
docker exec -it django_app python manage.py makemigrations

# Aplicar migraciones
docker exec -it django_app python manage.py migrate

# Migrar una app específica (ejemplo: assign)
docker exec -it django_app python manage.py makemigrations assign
docker exec -it django_app python manage.py migrate assign

# Crear superusuario (solo la primera vez)
docker exec -it django_app python manage.py createsuperuser

```

# Si agregas dependencias en requirements.txt, ejecuta:
docker-compose up --build
para instalar los nuevos paquetes automáticamente en el contenedor.


# Activar la tarea de manera manual 
# 1 entrar a la terminal de Django 
docker exec -it celery_worker python manage.py shell

# 2 Ejecutar los dos siguientes comandos 
 1  from apps.general.tasks import deactivate_expired_instructors
 2  deactivate_expired_instructors.delay()

# Revisar errores 
docker compose logs



redis-cli ping
respuesta correcta PONG

correr celerey
celery -A core worker --loglevel=info
celery -A core beat --loglevel=info  