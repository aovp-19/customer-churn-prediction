# api/Dockerfile

# Imagen base ligera de Python
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos primero solo requirements.txt (no todo el código)
# para aprovechar el cache de Docker: si no cambian las dependencias,
# no se reinstalan en cada build.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Ahora copiamos el resto del código de la API (main.py, model.pkl, etc.)
COPY . .

# Puerto en el que va a escuchar uvicorn dentro del contenedor
EXPOSE 8000

# Comando que arranca el servidor al iniciar el contenedor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]