FROM python:3.12.9-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install fastapi[standard]

COPY service/ ./service/

ENV LOG_PATH=/app/logs/responses.json

RUN mkdir -p /app/logs

# Exponer el puerto del servicio (ajusta si usas otro puerto)
EXPOSE 8000

# Comando para ejecutar FastAPI
CMD ["fastapi", "run", "service/main.py"]