# pull official base image
FROM python:3.8.3

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
#RUN apk update \
#    && apk add postgresql-dev gcc libressl-dev libffi-dev python3-dev musl-dev zlib-dev jpeg-dev cargo libmagic

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# copy project
COPY . .
RUN chmod +x ./entrypoint.sh
# run
ENTRYPOINT ["/app/entrypoint.sh"]
