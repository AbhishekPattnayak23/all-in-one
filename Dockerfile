# Stage 1 - build frontend
FROM node:20-alpine AS frontend_builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --ignore-scripts
COPY frontend/ ./
RUN npm run build

# Stage 2 - runtime
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ /app/backend
COPY --from=frontend_builder /app/frontend/dist /app/frontend/dist

EXPOSE 8000
CMD ["gunicorn", "backend.wsgi:application", "-b", "0.0.0.0:8000"]
