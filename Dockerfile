FROM python:3.11-slim

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio de trabajo
WORKDIR /app

# Dependencias del sistema (necesarias para mysqlclient y otros)
RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadb-dev \
    pkg-config \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el código fuente
COPY . .

# Copiar entrypoint y darle permisos
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
COPY wait-for-migrations.sh /app/wait-for-migrations.sh
RUN chmod +x /app/wait-for-migrations.sh

# Usar el entrypoint para esperar DB y ejecutar migraciones antes del comando
ENTRYPOINT ["/app/entrypoint.sh"]

# Comando por defecto (se puede sobreescribir en docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]