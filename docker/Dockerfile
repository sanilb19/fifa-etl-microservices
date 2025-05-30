FROM --platform=linux/arm64 python:3.12 as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libgmp-dev \
    libmpfr-dev \
    libmpc-dev \
    gcc \
    g++ \
    make \
    python3-dev \
    liblz4-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip and install wheel
RUN pip install --no-cache-dir --upgrade pip wheel setuptools

# Install base dependencies first
COPY requirements-base.txt .
RUN pip install --no-cache-dir -r requirements-base.txt

# Install optional dependencies with build isolation disabled 
COPY requirements-optional.txt .
RUN pip install --no-cache-dir --no-build-isolation -r requirements-optional.txt

# Final stage
FROM --platform=linux/arm64 python:3.12-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libgmp10 \
    libmpfr6 \
    libmpc3 \
    liblz4-1 \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy only necessary files
COPY config/ ./config/
COPY services/ ./services/
COPY .env* ./

# Set Python path and architecture-specific optimizations
ENV PYTHONPATH=/app
ENV DASK_DISTRIBUTED__WORKER__MEMORY__TARGET=0.6
ENV DASK_DISTRIBUTED__WORKER__MEMORY__SPILL=0.7
ENV DASK_DISTRIBUTED__WORKER__MEMORY__PAUSE=0.8
ENV DASK_DISTRIBUTED__WORKER__MEMORY__TERMINATE=0.95

# Create necessary directories
RUN mkdir -p /app/data/{raw,processed,archive,kagglehub}

# Default command
CMD ["python", "-m", "services.extract.main"]
