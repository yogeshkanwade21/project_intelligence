FROM python:3.13.5-slim-bookworm

# Set working directory
WORKDIR /app

ENV PYTHONPATH=/app

# Copy and install Python dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY app .

# Run server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
