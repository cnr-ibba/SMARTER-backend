.. SMARTER-backend documentation master file, created by
   sphinx-quickstart on Mon Sep 27 13:41:20 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to SMARTER-backend's documentation!
===========================================

This documentation describes how to install and interact with the SMARTER database
backend. If you need to access SMARTER data using a web browser, please see
`SMARTER database about page <https://webserver.ibba.cnr.it/smarter/about>`_.
If you need to access SMARTER data programmatically, please see
:ref:`Accessing SMARTER-backend`.

.. hint::

   We have a *R* package that can be used to interact with SMARTER-backend API,
   see `SMARTER R package <https://cnr-ibba.github.io/r-smarter-api/>`_ for more information.

About SMARTER-backend
---------------------

Briefly, the SMARTER database created and maintained with the
`SMARTER-database <https://github.com/cnr-ibba/SMARTER-database>`_ project is
made accessible to the community using this API. This API is the same used
by the `SMARTER-frontend <https://webserver.ibba.cnr.it/smarter/>`_ in
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
:ref:`Accessing SMARTER-backend` we describe how to programmatically access to data.

Citation
--------

If you use SMARTER data or any part of SMARTER software, please cite:

   Cozzi P, Manunza A, Ramirez-Diaz J, Tsartsianidou V, Gkagkavouzis K,
   Peraza P, Johansson A, Arranz J, Freire F, Kusza S, Biscarini F,
   Peters L, Tosser-Klopp G, Ciappesoni G, Triantafyllidis A, Rupp R,
   Servin B, Stella A (2024).
   SMARTER-database: a tool to integrate SNP array datasets for sheep and goat breeds.
   *GigaByte*.
   DOI: `10.46471/gigabyte.139 <https://doi.org/10.46471/gigabyte.139>`_

*BibTeX entry*:

.. code-block:: bibtex

   @Article{cozzi2024smarter,
     title = {SMARTER-database: a tool to integrate SNP array datasets for sheep and goat breeds},
     author = {Paolo Cozzi and Arianna Manunza and Johanna Ramirez-Diaz and Valentina Tsartsianidou and Konstantinos Gkagkavouzis and Pablo Peraza and Anna Maria Johansson and Juan José Arranz and Fernando Freire and Szilvia Kusza and Filippo Biscarini and Lucy Peters and Gwenola Tosser-Klopp and Gabriel Ciappesoni and Alexandros Triantafyllidis and Rachel Rupp and Bertrand Servin and Alessandra Stella},
     journal = {GigaByte},
     year = {2024},
     url = {https://github.com/cnr-ibba/SMARTER-database},
     doi = {10.46471/gigabyte.139},
   }

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
