# Use Python 3.11 (more stable than 3.12 for Railway)
FROM python:3.11-slim

WORKDIR /app

# Copy backend files
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Use entrypoint script
CMD ["sh", "entrypoint.sh"]
