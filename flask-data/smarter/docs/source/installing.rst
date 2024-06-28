
Backend installation
====================

.. toctree::
   :maxdepth: 4

Download SMARTER-backend from GitHub
------------------------------------

SMARTER-backend is available on `GitHub <https://github.com/cnr-ibba/SMARTER-backend.git>`_.
You can download the latest version of the code by running the following command:

.. code-block:: bash

   git clone https://github.com/cnr-ibba/SMARTER-backend.git

Install docker and docker-compose
---------------------------------

SMARTER-backend is a dockerized application. To run it, you need to install
`docker <https://docs.docker.com/get-docker/>`_ and
`docker-compose <https://docs.docker.com/compose/install/>`_. Please follow the
official installation instructions for your operating system.

Create a .env file
------------------

Before running the application, you need to create a ``.env`` file in the root directory
of the project. This is required to set the environment variables needed by the
application, like the database connection string. Create a ``.env`` file in the root
directory of the project with the following content:

.. code-block:: bash

   MONGODB_ROOT_USER=<mongodb root user>
   MONGODB_ROOT_PASS=<root pass>
   MONGODB_SMARTER_USER=<smarter user>
   MONGODB_SMARTER_PASS=<smarter pass>

Build the docker images
-----------------------

To build the docker images, run the following command:

.. code-block:: bash

   docker-compose build

Fix folder permissions
----------------------

Before running the application, you need to fix the permissions of the folders
where the application will store the data. Run the following command:

.. code-block:: bash

   chmod 777 mongodb-home/
   chmod o+t mongodb-home/
   docker-compose run --no-deps --rm uwsgi sh -c 'chgrp -R www-data .'
   cd flask-data/
   find . -type f -iname "*.py" -exec chmod g-w {} \;

Restore the database
--------------------

To restore the database, you need to download the latest dump from the
`SMARTER-database <https://github.com/cnr-ibba/SMARTER-database>`_
from the `FTP site <ftp://webserver.ibba.cnr.it/smarter/mongodb>`_.
Next, you have to place the dump in the `mongodb-home` folder and run
the following command:

.. code-block:: bash

   docker-compose run --rm mongo sh -c 'mongorestore --host mongo --username="${MONGO_INITDB_ROOT_USERNAME}" --password="${MONGO_INITDB_ROOT_PASSWORD}" --authenticationDatabase admin --db=smarter --drop --preserveUUID --gzip --archive= --archive=/home/mongodb/<SMARTER-database dump>'

Where ``<SMARTER-database dump>`` is the name of the mongodb dump file downloaded
from the FTP site.

Start the application
---------------------

To start the application, run the following command:

.. code-block:: bash

   docker-compose up -d
