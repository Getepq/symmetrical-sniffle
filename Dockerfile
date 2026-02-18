FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

COPY . .

mkdir -p data

VOLUME /app/data

ENV TOKEN="your_token_here" \
    PYTHONUNBUFFERED=1

# Запуск бота
CMD ["python", "main.py"]
