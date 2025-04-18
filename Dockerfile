# usings a minimal Python image
FROM python:3.11-slim
# setting workdir in the container
WORKDIR /app
# copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# copy app code
COPY app ./app
COPY tests ./tests
# exposing API port
EXPOSE 8000
# default command to run the FastAPI app (overridden in docker-compose when needed)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
