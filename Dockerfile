# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install GEMMA
RUN wget -O gemma.gz https://github.com/genetics-statistics/GEMMA/releases/download/v0.98.5/gemma-0.98.5-linux-static.gz \
    && gunzip gemma.gz \
    && chmod +x gemma \
    && mv gemma /usr/local/bin/gemma

# Copy project files
COPY . .

# Default command
CMD ["bash"]