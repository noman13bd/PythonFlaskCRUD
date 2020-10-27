# pull official base image
FROM python:3.8-slim-buster

# setting work directory
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /code/

EXPOSE 5000

CMD ["python", "./app.py", "runserver", "-h", "0.0.0.0", "-p", "5000"]