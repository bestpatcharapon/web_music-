# Use Python 3.11 (more stable than 3.12 for Railway)
FROM python:3.11-slim

WORKDIR /app

# Copy backend files
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./

# Set environment variables
ENV PORT=5000

# Run the application
CMD gunicorn app:app --bind 0.0.0.0:$PORT
