FROM python:3.9-slim-buster
ADD . /code
WORKDIR code
RUN apt-get update && apt-get -y install libpq-dev gcc
RUN pip install -r requirements.txt
CMD ["python", "create_tables.py"]