
FROM python:3.12


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat-openbsd
WORKDIR /code


COPY requirements.txt /code/


RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt


COPY . /code/


COPY ./entrypoint.sh /code/entrypoint.sh


RUN chmod +x /code/entrypoint.sh


ENTRYPOINT ["/code/entrypoint.sh"]
