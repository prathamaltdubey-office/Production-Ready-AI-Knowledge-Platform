FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-inference.txt .

RUN pip install --no-cache-dir \
    torch --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir -r requirements-inference.txt

COPY backend/ backend/
COPY chatbot/ chatbot/
COPY rag/ rag/
COPY src/ src/
COPY models/ models/
COPY documents/ documents/

RUN mkdir -p backend/logs

EXPOSE 8000

CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]
