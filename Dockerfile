FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim
RUN apt-get update
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./app /app
ENV PYTHONPATH=/
#CMD uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port $PORT
#CMD  uvicorn app.main:app --proxy-headers --host=0.0.0.0 --port=${80:-$PORT}

