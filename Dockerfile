FROM python:3.12.9-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install fastapi[standard]

COPY service/ ./service/

RUN mkdir -p logs

EXPOSE 8000

# Comando para ejecutar FastAPI
CMD ["fastapi", "run", "service/main.py"]