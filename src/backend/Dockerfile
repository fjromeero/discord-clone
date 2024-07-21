FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /app/

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

ENV PYTHONPATH=../app

COPY ./alembic.ini /app/

COPY ./app /app/app