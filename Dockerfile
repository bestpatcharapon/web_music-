# Use Python 3.11 (more stable than 3.12 for Railway)
FROM python:3.11-slim

WORKDIR /app

# Copy backend files
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./

# Railway will provide PORT environment variable, default to 8080
# Use shell form to properly expand variables
CMD gunicorn app:app --bind 0.0.0.0:${PORT:-8080} --workers 2 --timeout 120 --log-level info
