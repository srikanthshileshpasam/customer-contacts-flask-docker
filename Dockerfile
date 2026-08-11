FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Railway sets the PORT environment variable
ENV PORT=5000
EXPOSE $PORT

CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 app:app