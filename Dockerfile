FROM python:3.13-slim

RUN adduser --disabled-password --gecos '' appuser
WORKDIR /app


# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY templates ./templates

# Create data directory
RUN mkdir -p /app/data

# Declare volume for persistent data
VOLUME ["/app/data"]

# Expose port
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

RUN chown -R appuser:appuser /app/data
USER appuser

# Run the application with Gunicorn
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 300 --access-logfile - --error-logfile - app:app"]
