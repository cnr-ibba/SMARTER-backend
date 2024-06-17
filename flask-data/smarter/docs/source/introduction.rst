
Introduction
============

.. toctree::
   :maxdepth: 4

The SMARTER-backend is a `REST API service <https://en.wikipedia.org/wiki/Representational_state_transfer>`_
developed on top of the `SMARTER-database <https://github.com/cnr-ibba/SMARTER-database>`_
which provide methods to interact and access with SMARTER data using web resources.
By using SMARTER-backend, you can develop softwares or scripts which get access to
SMARTER data through web, without have a local instance of the SMARTER-database.
In a similar way a web-server receives a request from a web-browser and returns
text and images that could be rendered in a page, a REST API receives requests over the HTTP
protocol and returns data that could be read and manipulated by user softwares.

API endpoints
-------------

SMARTER-backend receives requests over the internet and returns SMARTER data in
JSON objects. There could be different data types that could be returned by
SMARTER-backend, for example Breed, Variant, Sample or Dataset. In order to access
to each different data types you have to make a request to the proper API
`endpoint <https://en.wikipedia.org/wiki/Web_API#Endpoints>`_, which is the mean
from which the API can access the resources requested. An API endpoint is an URL,
to which HTTP requests are submitted, and from which the response is thus expected.
For example, to retrieve information on all the Breeds stored in SMARTER database,
you should make a request to the breed endpoint which is::

   https://webserver.ibba.cnr.it/smarter-api/breeds

Similarly, to have informations on Goat samples you have to make a request to a different
endpoint, which is::

   https://webserver.ibba.cnr.it/smarter-api/samples/goat

If you inspect the two previous URL, you may notice that these two endpoint have
a prefix in common (``https://webserver.ibba.cnr.it/smarter-api``), while the last
part of the URL changes relying on the data they provide. There are a few endpoints
available by SMARTER-backend:

+------------------------+---------------+-----------------------------------------------+
| Suffix                 | Data type     | Description                                   |
+========================+===============+===============================================+
| /auth/login            | Users         | user authentication (No more required)        |
+------------------------+---------------+-----------------------------------------------+
| /breeds                | Breeds        | returns a list of the available breeds        |
+------------------------+---------------+-----------------------------------------------+
| /datasets              | Dataset       | returns a list of the available datasets      |
+------------------------+---------------+-----------------------------------------------+
| /info                  | SmarterInfo   | A dictionary of smarter information           |
+------------------------+---------------+-----------------------------------------------+
| /samples/sheep         | SampleSheep   | returns a list of the sheep samples           |
+------------------------+---------------+-----------------------------------------------+
| /samples/goat          | SampleGoat    | returns a list of goat samples                |
+------------------------+---------------+-----------------------------------------------+
| /samples.geojson/sheep | GeoJSON       | return sheep samples in GeoJSON format        |
+------------------------+---------------+-----------------------------------------------+
| /samples.geojson/goat  | GeoJSON       | return goat samples in GeoJSON format         |
+------------------------+---------------+-----------------------------------------------+
| /supported-chips       | SupportedChip | returns a list of chip which provide SNPs     |
|                        |               | to the SMARTER dataset                        |
+------------------------+---------------+-----------------------------------------------+
| /variants/sheep/OAR3   | VariantSheep  | returns a list of sheep SNPs in OAR3 assembly |
+------------------------+---------------+-----------------------------------------------+
| /variants/sheep/OAR4   | VariantSheep  | returns a list of sheep SNPs in OAR4 assembly |
+------------------------+---------------+-----------------------------------------------+
| /variants/goat/ARS1    | VariantGoat   | returns a list of goat SNPs in ARS1 assembly  |
+------------------------+---------------+-----------------------------------------------+
| /variants/goat/CHI1    | VariantGoat   | returns a list of goat SNPs in CHI1 assembly  |
+------------------------+---------------+-----------------------------------------------+

So if you require to retrieve all the sheep SNPs in OAR3 assembly,
you can append the suffix ``/variants/sheep/OAR3``
to the common prefix ``https://webserver.ibba.cnr.it/smarter-api`` to obtain the
final endpoint::

   https://webserver.ibba.cnr.it/smarter-api/variants/sheep/OAR3

Every endpoints described provide a list of results, however you could retrieve a
specific object by appending the proper ObjectId to the endpoint, for example::

   https://webserver.ibba.cnr.it/smarter-api/datasets/604f75a61a08c53cebd09b5b

will retrieve the dataset with ObjectId ``604f75a61a08c53cebd09b5b``.

.. warning::

   Please note that ObjectId could change over time, since they rely on the time
   they are added into database. If you require a particular data,
   you should use the proper API endpoint by providing the appropriate parameters
   as arguments, for example ``file=<file name>`` to retrieve the dataset relying
   on provided file name.

HTTP Verbs
----------

An endpoint can act differently relying on the
`HTTP Verb <https://www.restapitutorial.com/lessons/httpmethods.html>`_ used when
making a request. For SMARTER-backend, only two HTTP Verbs (or methods) are currently
supported, ``GET`` and ``POST``:

+-----------+--------+-----------------------------------------------+
| Http Verb | CRUD   |                                               |
+===========+========+===============================================+
| GET       | Read   | Retrieve a list of objects or a single object |
+-----------+--------+-----------------------------------------------+
| POST      | Create | add a payload to a query                      |
+-----------+--------+-----------------------------------------------+

More precisely, SMARTER data through the SMARTER-backend are read-only and
``GET`` and ``POST`` method are allowed in order to retrieve any type of SMARTER
data object from the API. ``POST`` method are required to submit complex queries
by providing a payload to certain endpoints.

Status codes
------------

SMARTER-backend API uses standard response status code to show the outcome of
each HTTP request. Briefly, replies with a status code like ``2xx`` are successful
requests, ``4xx`` codes means errors in client side (you are using the API in the
wrong way) and ``5xx`` means errors on the server side (you should get in touch
with API maintainer and describe what went wrong).
You can find a complete reference on HTTP status codes
`here <https://www.restapitutorial.com/httpstatuscodes.html>`_.

+----------------------------+-----------------------------------------------------+
| Status Code                | Description                                         |
+============================+=====================================================+
| 200 Ok                     | A request completed with success                    |
+----------------------------+-----------------------------------------------------+
|| 400 Bad request           || The request was malformed. The response body will  |
||                           || include an error providing further information     |
+----------------------------+-----------------------------------------------------+
| 404 Not Found              | Requested object or endpoint doesn't exist          |
+----------------------------+-----------------------------------------------------+
|| 500 Internal Server Error || The server encountered an unexpected condition     |
||                           || which prevented it from fulfilling the request     |
+----------------------------+-----------------------------------------------------+

Authentication (No more required)
---------------------------------

After the public release of SMARTER data, the authentication process has been
removed and now you can access to SMARTER data without providing any credentials.
The *auth* endpoint is still available, but it will return a 200 status code
with a standard message regardless of the credentials you provide. This is
required to maintain compatibility with the previous version of the API clients,
but it is not required to generate a token to get access to SMARTER data.
The old endpoint is available at the following URL by providing a ``POST`` request::

   https://webserver.ibba.cnr.it/smarter-api/auth/login
