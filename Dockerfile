# --- Stage 1: Builder ---
FROM python:3.10-slim as builder

WORKDIR /app

# Only install build tools needed for pip compilation
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Install to a local directory to copy easily in stage 2
RUN pip install --no-cache-dir --user -r requirements.txt


# --- Stage 2: Final Runtime ---
FROM python:3.10-slim

WORKDIR /app

# Optimized dependencies for OpenUSD Headless Processing
# We keep only the bare essentials for shared object loading
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the installed python packages from the builder stage
COPY --from=builder /root/.local /root/.local
COPY . .

# Ensure the local bin is in path
ENV PATH=/root/.local/bin:$PATH
ENV AZURE_QUANTUM_CONNECTION_STRING=""

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]