FROM python:3.15-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_TIMEOUT=100 PIP_RETRIES=5
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 100 --retries 5 -r requirements.txt
COPY src ./src
COPY tests ./tests
COPY docs ./docs
COPY data ./data
COPY README.md .
ENV PYTHONPATH=/app/src
CMD ["pytest", "-q"]
