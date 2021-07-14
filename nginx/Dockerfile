
#
# VERSION 0.1
# DOCKER-VERSION  20.10.6
# AUTHOR:         Paolo Cozzi <cozzi@ibba.cnr.it>
# DESCRIPTION:    A nginx container to work with flask
#

# Get the last stable nginx image
FROM nginx:1.20

LABEL maintainer="Paolo Cozzi <paolo.cozzi@ibba.cnr.it>" \
      description="A nginx container to work with flask" \
      version="0.1"

# synchronize timezone for container
# https://forums.docker.com/t/synchronize-timezone-from-host-to-container/39116
RUN echo "Europe/Rome" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

# Copy nginx configuration file in conf.d directory
COPY nginx.conf /etc/nginx/nginx.conf

# define NGINX volume
VOLUME /etc/nginx/conf.d/
