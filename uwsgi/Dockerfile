
#
# VERSION 0.1
# DOCKER-VERSION  20.10.6
# AUTHOR:         Paolo Cozzi <cozzi@ibba.cnr.it>
# DESCRIPTION:    A flask container working on flask
#

# start from a python base image
FROM python:3.9.5

MAINTAINER Paolo Cozzi <cozzi@ibba.cnr.it>

# synchronize timezone for container
# https://forums.docker.com/t/synchronize-timezone-from-host-to-container/39116
RUN echo "Europe/Rome" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

# Create directory for a django project
RUN mkdir /var/uwsgi/

# Set corrent working directory
WORKDIR /var/uwsgi/

# Set uwsgi directory as VOLUME
VOLUME /var/uwsgi/

# Expose the default port for flask
EXPOSE 5000

# This environment variable force stdin, stdout and stderr to be totally unbuffered
ENV PYTHONUNBUFFERED 1

# Install pypi modules (uwsgi)
COPY requirements.txt /root/
RUN pip install --no-cache-dir -r /root/requirements.txt

# Execute a default command
CMD ["/bin/bash"]
