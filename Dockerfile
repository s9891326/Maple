ARG PYTHON_VERSION=3.7

FROM python:${PYTHON_VERSION}

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-setuptools \
    python3-wheel

RUN mkdir -p /app

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

EXPOSE 8000

#RUN chmod +x ./start.sh

#CMD [ "/bin/bash", "./start.sh", "start" ]
CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "Maple.wsgi"]
