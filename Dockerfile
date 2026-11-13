FROM python:3.11-slim
WORKDIR /app
ENV PYTHONPATH=/app/src:/app PYTHONUNBUFFERED=1
COPY requirements.txt requirements-ui.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-ui.txt
COPY src ./src
COPY api ./api
COPY monitoring ./monitoring
COPY frontend ./frontend
COPY configs ./configs
COPY data/eval ./data/eval
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
