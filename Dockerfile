# Stage 1: Build the React Frontend
FROM node:18-alpine AS builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Build the Python Backend
FROM python:3.12-slim

# --- NEW LINE ADDED ---
# This is a standard best practice that prevents Python from buffering output,
# making logs appear instantly. It also forces Railway to do a fresh build.
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copy ONLY the requirements file first for caching optimization
COPY ./backend/requirements.txt .

# Install all Python dependencies
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

# Now, copy all of your application code
COPY ./backend ./backend
COPY --from-builder /app/frontend/build ./frontend/build

# Set the final command to run the server
CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8080"]