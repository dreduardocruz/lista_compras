FROM python:3.9

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    gfortran \
    musl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies in specific order
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir wheel setuptools && \
    pip install --no-cache-dir numpy==1.19.5 && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]