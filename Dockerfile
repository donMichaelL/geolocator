# Specify the image of the Docker Container
# Search in dockerhub.com
#FROM thinkwhere/gdal-python
FROM python:3.5

# (optional) the name of the maintener
LABEL maintainer="Michael Loukeris"

# The environment variables
# The PYTHONUNBUFFERED ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin libsqlite3-mod-spatialite


# Add dependencies
COPY ./requirements.txt /requirements.txt

# Execute commands as if you were executing it in a terminal
RUN pip install -r /requirements.txt

RUN mkdir /roborder
WORKDIR /roborder
COPY ./ /roborder

CMD ["python", "manage.py", "runserver", "0:8000"]

