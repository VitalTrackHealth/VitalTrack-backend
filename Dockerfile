### SET UP STAGE ##############################################################

FROM python:3.10-slim

WORKDIR /app

### BUILD STAGE ###############################################################

RUN apt-get update && apt-get install --yes \
    curl \
    &&\
    # Clean unused apt packages, configurations, and cache
    apt-get purge --yes --auto-remove &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*
    
# Install PDM and sync dependency files
RUN python3 -m pip install --no-cache-dir pdm    
COPY pyproject.toml pdm.lock ./

# Install dependencies
RUN pdm sync

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["pdm", "run", "dev", "--host", "0.0.0.0", "--port", "8000"]
