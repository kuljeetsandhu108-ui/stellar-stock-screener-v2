# Stage 1: Build the React Frontend
# We start with a lightweight Node.js image
FROM node:18-alpine AS builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Build the Python Backend and Serve the App
# We start with an official Python image
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies (not strictly needed now, but good practice)
RUN apt-get update && apt-get install -y --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install them
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy the backend source code
COPY ./backend ./backend

# Copy the BUILT frontend from the 'builder' stage
COPY --from=builder /app/frontend/build ./frontend/build

# Tell the world that port 10000 is open
EXPOSE 10000

# Set the command to run the Uvicorn server
# Note: Railway provides the $PORT variable, so we use it.
CMD uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT