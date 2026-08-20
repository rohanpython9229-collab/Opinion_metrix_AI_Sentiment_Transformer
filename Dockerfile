# Use Python 3.11
FROM python:3.11-slim

# Prevent Python from creating .pyc files
# and show logs immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install PostgreSQL dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install CPU-only PyTorch
RUN pip install --no-cache-dir \
    torch==2.13.0 \
    --index-url https://download.pytorch.org/whl/cpu

# Install remaining dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Render will provide the PORT variable
EXPOSE 8000

# Make startup script executable
RUN chmod +x start.sh

# Start FastAPI
CMD ["./start.sh"]