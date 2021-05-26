# SMARTER-backend
SMARTER Backend API

[![Build Status](https://www.travis-ci.com/cnr-ibba/SMARTER-backend.svg?branch=master)](https://www.travis-ci.com/cnr-ibba/SMARTER-backend)
[![Coverage Status](https://coveralls.io/repos/github/cnr-ibba/SMARTER-backend/badge.svg?branch=master)](https://coveralls.io/github/cnr-ibba/SMARTER-backend?branch=master)

Setting the `.env` file
-----------------------

`docker-compose` can read variables from a `.env` placed in the working directory.
Here we will define all variables useful for our containers, like database password.
Edit a new `.env` file in working directory and set passwords for such environment
variables:

```
MONGODB_ROOT_USER=<root user>
MONGODB_ROOT_PASS=<root pass>
MONGODB_SMARTER_USER=<smarter user>
MONGODB_SMARTER_PASS=<smarter pass>
```

> *TODO*: manage sensitive data using secret in docker-compose, as described
[here](https://docs.docker.com/engine/swarm/secrets/#use-secrets-in-compose) and
[here](https://docs.docker.com/compose/compose-file/#secrets)

Setting the proper permissions
------------------------------

Set `mongodb-home` folder permissions with:

```
$ chmod 777 mongodb-home/
$ chmod o+t mongodb-home/
```

Add a smarter user
------------------

Add a smarter user by calling a *flask script*:

```
$ docker-compose run --rm uwsgi flask users create smarter
```

Connect to mongodb
------------------

```
$ docker-compose run --rm --user mongodb mongo sh -c 'mongo --host mongo --username="${MONGO_INITDB_ROOT_USERNAME}" --password="${MONGO_INITDB_ROOT_PASSWORD}"'
```
