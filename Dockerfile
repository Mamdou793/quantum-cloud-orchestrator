# Use an official lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies for pxr (USD) and common build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libglu1-mesa \
    libgl1 \
    libxrender1 \
    libxcursor1 \
    libxft2 \
    libxinerama1 \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements first (to leverage Docker's cache)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Set environment variables (Placeholder for your Connection String)
# Note: In production, we pass these at runtime, not in the file!
ENV AZURE_QUANTUM_CONNECTION_STRING=""

# The command to run your simulation
CMD ["python", "test_quantum.py"]