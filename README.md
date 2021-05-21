# SMARTER-backend
SMARTER Backend API

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
