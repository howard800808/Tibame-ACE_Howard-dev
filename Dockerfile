FROM python:3.12-slim

# Use a simple, reproducible build that installs from requirements.txt
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app

# system deps required for some packages (adjust as needed)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc libpq-dev libgl1 libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /usr/src/app

ENV PYTHONPATH=/usr/src/app \
    PYTHONOPTIMIZE=1

# Expose the FastAPI port
EXPOSE 8000

# Default command (can be overridden by docker-compose)
# CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000"]
