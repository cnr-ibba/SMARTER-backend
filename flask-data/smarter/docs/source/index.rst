.. SMARTER-backend documentation master file, created by
   sphinx-quickstart on Mon Sep 27 13:41:20 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to SMARTER-backend's documentation!
===========================================

This documentation describes how to install and interact with the SMARTER database
backend. Briefly, the SMARTER database created and maintained with the
`SMARTER-database <https://github.com/cnr-ibba/SMARTER-database>`_ project is
made accessible to SMARTER partners using this API. This API is the same used
by the `SMARTER-frontend <https://github.com/cnr-ibba/SMARTER-frontend>`_ in
order to access and browse SMARTER data using a web browser.

SMARTER-backend is a `flask-API <https://flask.palletsprojects.com/en/2.0.x/>`_
application developed on top of a `MongoDB <https://www.mongodb.com/>`_ instance.
The application works inside `Docker <https://www.docker.com/>`_ containers
managed with `docker-compose <https://docs.docker.com/compose/>`_.
Users who need to subset or retrieve genotypes from the entire genotypes dataset
need to retrieve first variants and samples according their needs, in order to filter out
the data they need using a `PLINK <https://zzz.bwh.harvard.edu/plink/>`_ command line.

Documentation is organized as following: in :ref:`Introduction` we describe what
SMARTER-backend is and we provide general information. In :ref:`Backend installation`
we describe how to install a local instance of SMARTER-backend. Then in
:ref:`Accessing SMARTER-backend` we describe how to programmatically access to data
or how to inspect data using applications like `Postman <https://www.postman.com/>`_
or `Talend Api Tester <https://chrome.google.com/webstore/detail/talend-api-tester-free-ed/aejoelaoggembcahagimdiliamlcdmfm>`_
google-chrome extension.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Documentation Contents
----------------------

.. toctree::
   :maxdepth: 2

   introduction
   installing
   accessing
   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
