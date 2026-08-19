# Use Python 3.11 because the project uses Python 3.11
FROM python:3.11-slim

# Prevent Python from creating .pyc files
# and make Python output appear immediately in Docker logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install PostgreSQL client dependencies
# required by psycopg2-binary / PostgreSQL connectivity
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
# This helps Docker cache dependency installation
COPY requirements.txt .

# Install the same PyTorch version used by the project
# from the CPU-only PyTorch wheel repository
RUN pip install --no-cache-dir \
    torch==2.13.0 \
    --index-url https://download.pytorch.org/whl/cpu

# Install remaining Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the complete project into the container
COPY . .

# Streamlit port
EXPOSE 8501

# FastAPI port
EXPOSE 8000

COPY start.sh .

CMD ["sh", "start.sh"]

EXPOSE 8501
EXPOSE 8000

COPY start.sh .

RUN chmod +x start.sh

CMD ["./start.sh"]
