
#
# VERSION 0.3
# DOCKER-VERSION  24.0.6
# AUTHOR:         Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
# DESCRIPTION:    A flask container working with mongoengine
#

###############################################################################
# 1st build stage

# inspired from https://bmaingret.github.io/blog/2021-11-15-Docker-and-Poetry
# Those variables are defined before the FROM scope: to use them after, recall
# ARG in build stages
ARG APP_NAME=SMARTER-backend
ARG APP_PATH=/opt/$APP_NAME
ARG PYTHON_VERSION=3.11
ARG POETRY_VERSION=1.8.3

FROM python:${PYTHON_VERSION}

LABEL maintainer="Paolo Cozzi <paolo.cozzi@ibba.cnr.it>" \
      description="A flask container working with mongoengine" \
      version="0.3"

# Import ARGs which I need in this build stage
# IMPORTANT!: without this redefinition, you can't use variables defined
# before the first FROM statement
ARG POETRY_VERSION
ARG APP_NAME
ARG APP_PATH

# Set some useful variables
ENV \
      PYTHONDONTWRITEBYTECODE=1 \
      PYTHONUNBUFFERED=1 \
      PYTHONFAULTHANDLER=1
ENV \
      POETRY_VERSION=${POETRY_VERSION} \
      POETRY_HOME="/opt/poetry" \
      POETRY_VIRTUALENVS_CREATE=1 \
      POETRY_VIRTUALENVS_IN_PROJECT=true \
      POETRY_NO_INTERACTION=1

# Install Poetry - require $POETRY_VERSION & $POETRY_HOME environment variables
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="$POETRY_HOME/bin:$PATH"

# CREATE APP_PATH
RUN mkdir -p ${APP_PATH}
WORKDIR ${APP_PATH}

# Need to copy all the files declared in pyproject.toml
COPY ../poetry.lock ../pyproject.toml ../README.md ./

# Install stuff
RUN poetry install

###############################################################################
# 2nd build stage

FROM python:${PYTHON_VERSION}-slim

LABEL maintainer="Paolo Cozzi <paolo.cozzi@ibba.cnr.it>" \
      description="A flask container working with mongoengine" \
      version="0.3"

# Import ARGs which I need in this build stage
# IMPORTANT!: without this redefinition, you can't use variables defined
# before the first FROM statement
ARG APP_PATH
ARG VIRTUAL_ENV=${APP_PATH}/.venv

# synchronize timezone for container
# https://forums.docker.com/t/synchronize-timezone-from-host-to-container/39116
RUN echo "Europe/Rome" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

# install required packages
RUN apt-get update && apt-get install -y \
      libxml2 \
      git \
      && rm -rf /var/lib/apt/lists/*

# set safe directory for uwsgi
RUN git config --global --add safe.directory /var/uwsgi

# Set some useful variables
ENV \
      PYTHONUNBUFFERED=1 \
      PYTHONFAULTHANDLER=1
# See https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV \
      VIRTUAL_ENV=${VIRTUAL_ENV} \
      PATH="${VIRTUAL_ENV}/bin:${PATH}"

# copy the application from build stage
COPY --from=0 ${APP_PATH} ${APP_PATH}

# Set poetry APP directory as VOLUME
VOLUME ${APP_PATH}

# Expose the default port
EXPOSE 8000

# This environment variable force stdin, stdout and stderr to be totally unbuffered
ENV PYTHONUNBUFFERED 1

# Create directory for a uwsgi project
RUN mkdir /var/uwsgi/

# Set corrent working directory
WORKDIR /var/uwsgi/

# Set uwsgi directory as VOLUME
VOLUME /var/uwsgi/

# Expose the default port for flask
EXPOSE 5000

# This environment variable force stdin, stdout and stderr to be totally unbuffered
ENV PYTHONUNBUFFERED 1

# Execute a default command
CMD ["/bin/bash"]
