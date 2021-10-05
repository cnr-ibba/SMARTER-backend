
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
protocol and returns data that could be readed and manipolated by user softwares.

API endpoints
-------------

SMARTER-backend receives requests over the internet and returns SMARTER data in 
JSON objects. There could be different data types that could be returned by 
SMARTER-backend, for example Breed, Variant, Sample or Dataset. In order to access 
to each different data types you have to make a request to the proper API 
`endpoint <https://en.wikipedia.org/wiki/Web_API#Endpoints>`_, which is the means
from which the API can access the resources requested. An API endpoint is an URL,
to which HTTP requests are submitted, and from which the response is thus expected.
For example, to retrieve information on all the Breeds stored in SMARTER database, 
you should make a request to the breed endpoint which is::

   https://webserver.ibba.cnr.it/smarter-api/breeds

while, to have informations on Goat samples you have to make a request to a different
endpoint, which is::

   https://webserver.ibba.cnr.it/smarter-api/samples/goat

If you inspect the two previous URL, you may notice that these two endpoint have 
a prefix in common (``https://webserver.ibba.cnr.it/smarter-api``), while the last 
part of the URL changes relying on the data they provide. There are a few endpoints 
available by SMARTER-backend:

+-------------------+----------------+--------------------------------------------+
| Suffix            | Data type      | Description                                |
+===================+================+============================================+
| /breeds           | Breeds         | returns a list of the available breeds     |
+-------------------+----------------+--------------------------------------------+
| /datasets         | Dataset        | returns a list of the available datasets   |
+-------------------+----------------+--------------------------------------------+
|| /supported-chips || SupportedChip || returns a list of chip which provide SNPs |
||                  ||               || to the SMARTER dataset                    |
+-------------------+----------------+--------------------------------------------+
| /samples/sheep    | SampleSheep    | returns a list of the sheep samples        |
+-------------------+----------------+--------------------------------------------+
| /samples/goat     | SampleGoat     | returns a list of goat samples             |
+-------------------+----------------+--------------------------------------------+
| /variants/sheep   | VariantSheep   | returns a list of sheep SNPs               |
+-------------------+----------------+--------------------------------------------+
| /variants/goat    | VariantGoat    | returns a list of goat SNPs                |
+-------------------+----------------+--------------------------------------------+

So if you require to retrieve all the sheep SNPs, you can append the suffix ``/variants/sheep``
to the common prefix ``https://webserver.ibba.cnr.it/smarter-api`` to obtain the 
final endpoint::

   https://webserver.ibba.cnr.it/smarter-api/variants/sheep

Every endpoint described provide a list of results, however you could retrieve a 
specific object by appending the proper ObjectId to the endpoint, for example::

   https://webserver.ibba.cnr.it/smarter-api/datasets/604f75a61a08c53cebd09b5b

will retrieve the dataset with ObjectId ``604f75a61a08c53cebd09b5b``.

.. warning:: 
   
   Please note that ObjectId could change over time, since they rely on the time 
   they are added into database. If you require a particolular data, 
   you should use the proper API endpoint by providing the appropriate parameters
   as arguments, for example ``file=<file name>`` to retrieve the dataset relying 
   on provided file name.

HTTP Verbs
----------

An endpoint can act differently relying on the 
`HTTP Verb <https://www.restapitutorial.com/lessons/httpmethods.html>`_ used when 
making a request. For SMARTER-backend, only two HTTP Verbs (or methods) are currently 
supported, ``GET`` and ``POST``:

+-----------+--------+------------------------------------+
| Http Verb | CRUD   |                                    |
+===========+========+====================================+
| GET       | Read   | Retrieve a list or a single object |
+-----------+--------+------------------------------------+
| POST      | Create | Create a new auth token            |
+-----------+--------+------------------------------------+

More precisely, SMARTER data through the SMARTER-backend are read-only and only 
``GET`` method are allowed in order to retrieve any type of SMARTER
data object from the API. ``POST`` method are required only during the authentication
step, in order to generate a JWT token required to access to the SMARTER information

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
|| 401 UnAuthorized          || Request lacks of the required authorization header |
||                           || or token is expired                                |
+----------------------------+-----------------------------------------------------+
| 404 Not Found              | Requested object or endpoint doesn't exist          |
+----------------------------+-----------------------------------------------------+
|| 500 Internal Server Error || The server encountered an unexpected condition     |
||                           || which prevented it from fulfilling the request     |
+----------------------------+-----------------------------------------------------+

JWT Authentication
------------------

.. epigraph::

   JSON Web Token (JWT) is an open standard (RFC 7519) that defines a compact and 
   self-contained way for securely transmitting information between parties as a 
   JSON object. This information can be verified and trusted because it is 
   digitally signed (`<https://jwt.io/introduction>`_)

SMARTER data aren't available to the public yet, only SMARTER WP4 should have the 
credentials to use the SMARTER-backend API. If you are a WP4 member and you don't 
have the required credentials, please get in touch with WP4 group leaders. 
In order to get access to SMARTER data, you are required to generate a JWT token 
by providing your credentials as a ``POST`` request to the API authentication endpoint, 
which is::

   https://webserver.ibba.cnr.it/smarter-api/auth/login

If you credentials are valid, you will receive a JSON object with your generated 
token and an expires date. By default a token will be valid for 7 days after it was 
generated. You need to add this token as an Authorization header to all of your 
API requests. The format is ``Authorization: Bearer <your token>``. In the 
:ref:`Accessing SMARTER-backend` section you will find furter instructions on 
how to generate your token and how you could interact with the SMARTER-backend 
API.

.. danger:: 

   Please don't share your API credentials or the generated token with anyone,
   this includes also code that could be shared using github: credentials or 
   generated tokens should be never stored in your code
