
Accessing SMARTER-backend
=========================
The SMARTER-backend is a RESTful API, which means that it's a web service that
provides access to its resources via HTTP requests. The API is designed to be
simple and easy to use, and it's based on the `JSON <https://www.json.org/json-en.html>`_
data format, which is a lightweight data-interchange format that is easy for
humans to read and write and easy for machines to parse and generate.

Query parameters
----------------

The :ref:`API endpoints` described in the :ref:`Introduction` return by default
all the SMARTER objects they managed. However it's possible to filter out the
results returned using ``GET`` parameters (also called URL parameters or
`query strings <https://en.wikipedia.org/wiki/Query_string>`_) which are usually
name-value pairs, separated by an ``=`` sign. For example, by submitting a request
to::

   https://webserver.ibba.cnr.it/smarter-api/breeds

You will get all the Breeds stored in smarter database, but you can filter out
the results by species by passing ``species=Goat`` parameter::

   https://webserver.ibba.cnr.it/smarter-api/breeds?species=Goat

Please note that parameters are not part of the API endpoint: The question mark
is used as a separator, and divide the endpoint from the ``GET`` parameter. You
can provide multiple parameters by joining them with the ``&`` character, for
example::

   https://webserver.ibba.cnr.it/smarter-api/breeds?species=Goat&search=land

will retrive all the SMARTER goat breeds which have ``land`` in ther name (*Landrace*,
for example, but also *Rangeland*)

.. hint::

   The page https://webserver.ibba.cnr.it/smarter-api/docs/ describes every API
   endpoints with their own set of parameters, see the proper endpoint
   documentation to have a list of the allowed parameters and what they do.

Pagination
----------

API queries could returned thousands of results, so to improve performance and
lower traffic between client and server, all the API endpoints implements pagination.
This means that each query returns a limited set of results, but it returns also
the total number of objects with informations useful to collect the next batch
of objects. For example, if you analyze the breed API response while search for
all the objects (``https://webserver.ibba.cnr.it/smarter-api/breeds``), you will
see a reply like this::

   {
      "items": [
         ...
      ],
      "next": "/smarter-api/breeds?size=10&page=2",
      "page": 1,
      "pages": 26,
      "prev": null,
      "size": 10,
      "total": 257
   }

Where in the ``items`` array there will be ``size`` Breed objects (default 10,
omitted here to better describe the response); in the ``next`` attribute there
will be the URLs to be used to get the next batch of  objects, if you
get the next page, you will get a ``prev`` attribute for the previous page;
The ``total`` stands for the total number of breed objects and the ``page``
stands for the current batch page number. By default, the behaviour is to
display 10 results per page, however you could change this by setting a different
page size with a get parameter, for example ``size=20``.

.. warning::

   Please remember that pagination helps to better manage resources, don't
   try to retrieve all the results for a single query request: there could be
   a size limit or you can have issues in retrieve / process the results

Examples
--------

Here we list some patterns on how to interact with the SMARTER-backend, feel free
to follow the method you prefer:

.. toctree::
   :maxdepth: 4

   accessing/thirdy-party
   accessing/python
   accessing/r
