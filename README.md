# SMARTER-backend

SMARTER Backend API

[![Build Status](https://www.travis-ci.com/cnr-ibba/SMARTER-backend.svg?branch=master)](https://www.travis-ci.com/cnr-ibba/SMARTER-backend)
[![Coverage Status](https://coveralls.io/repos/github/cnr-ibba/SMARTER-backend/badge.svg?branch=master)](https://coveralls.io/github/cnr-ibba/SMARTER-backend?branch=master)
[![Documentation Status](https://readthedocs.org/projects/smarter-backend/badge/?version=latest)](https://smarter-backend.readthedocs.io/en/latest/)

## Setting the `.env` file

`docker-compose` can read variables from a `.env` placed in the working directory.
Here we will define all variables useful for our containers, like database password.
Edit a new `.env` file in working directory and set passwords for such environment
variables:

```text
MONGODB_ROOT_USER=<root user>
MONGODB_ROOT_PASS=<root pass>
MONGODB_SMARTER_USER=<smarter user>
MONGODB_SMARTER_PASS=<smarter pass>
JWT_SECRET_KEY=<secret key>
```

> *TODO*: manage sensitive data using secret in docker-compose, as described
[here](https://docs.docker.com/engine/swarm/secrets/#use-secrets-in-compose) and
[here](https://docs.docker.com/compose/compose-file/#secrets)

### Genereate the JWT secret key

[Here](https://stackoverflow.com/a/23728630/4385116) you can find hints on
how to define a secret key with python:

```python
import string
import secrets
print(''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(50)))
```

## Setting the proper permissions

Set `mongodb-home` folder permissions with:

```bash
chmod 777 mongodb-home/
chmod o+t mongodb-home/
```

Fix `flask-data` permissions:

```bash
docker-compose run --no-deps --rm uwsgi sh -c 'chgrp -R www-data .'
cd flask-data/
find . -type f -iname "*.py" -exec chmod g-w {} \;
```

## Add a smarter user

Add a smarter user by calling a *flask script*:

```bash
docker-compose run --rm uwsgi flask users create smarter
```

## Connect to mongodb

```bash
docker-compose run --rm --user mongodb mongo sh -c 'mongo --host mongo --username="${MONGO_INITDB_ROOT_USERNAME}" --password="${MONGO_INITDB_ROOT_PASSWORD}"'
```

## Import data into database

Execute a `mongodump` of an instance of the
[SMARTER-database](https://github.com/cnr-ibba/SMARTER-database) project, for
example:

```bash
docker-compose run --rm --user mongodb mongo sh -c 'DATE=$(date +%Y-%m-%d); mongodump --host mongo --username="${MONGO_INITDB_ROOT_USERNAME}" --password="${MONGO_INITDB_ROOT_PASSWORD}" --authenticationDatabase admin --db=smarter --gzip --archive=/home/mongodb/${DATE}\_smarter.archive.gz'
```

Then copy (or move) the dump file into `mongodb-home` folder of this project. You
can restore the database using `mongorestore`, for example:

```bash
docker-compose run --rm --user mongodb mongo sh -c 'mongorestore --host mongo --username="${MONGO_INITDB_ROOT_USERNAME}" --password="${MONGO_INITDB_ROOT_PASSWORD}" --authenticationDatabase admin --db=smarter --drop --preserveUUID --gzip --archive=/home/mongodb/2021-06-18_smarter.archive.gz'
```

## Monitoring UWSGI processes

Enter inside uwsgi container (with `docker-compose exec`), then monitor uwsgi with
[uwsgitop](https://github.com/xrmx/uwsgitop):

```bash
docker-compose exec uwsgi bash
uwsgitop /tmp/smarter-stats.sock
```

Type `q` to exit from monitoring process
