FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/data
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser
VOLUME ["/app/data"]
CMD ["python", "main.py"]
