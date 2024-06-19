
Accessing data using Python
===========================

.. toctree::
   :maxdepth: 4

Here are some examples of how to access data using Python. You can find a similar
example for ``R`` in the :ref:`Accessing data using R` section.

Importing packages
------------------

First we need to import the packages we will be using. We will be using ``requests``
to download the data from the internet and some utility functions to deal with
urls. Eventually, we will transform data into a ``pandas`` DataFrame.

.. code-block:: python

   import json
   import requests

   import pandas as pd
   from urllib.parse import urljoin

Deal with data and pagination in python
---------------------------------------

We can define some utility functions to deal with data and pagination:

.. code-block:: python

   base_url = "https://webserver.ibba.cnr.it"
   session = requests.Session()


   def read_url(session, url, params={}):
      response = session.get(url, params=params)

      # check errors: SMARTER-backend is supposed to return JSON objects
      if response.headers['Content-Type'] != 'application/json':
         raise Exception("API did not return json")

      # parse json data
      parsed = response.json()

      # check for errors
      if response.status_code != 200:
         raise Exception(
            f"SMARTER API returned an error [{response.status_code}]: "
            f"'{parsed['message']}'")

      return parsed


   def get_smarter_data(url, params={}, session=session):
      # do the request and parse data with our function
      parsed = read_url(session, url, params)

      # track results
      results = parsed["items"]

      # check for pagination
      while parsed["next"]:
         # append next value to base url
         url = urljoin(base_url, parsed["next"])

         # query arguments are already in url: get next page
         parsed = read_url(session, url)

         # append new results to results list
         results += parsed["items"]

      return results


``base_url`` is the base url of the SMARTER API. We define a ``session`` to keep track of
the cookies and headers of the requests. We define a function ``read_url`` that
parses the response of the API and checks for errors. We define a function
``get_smarter_data`` that gets the data from the API and checks for pagination.

Read data with Python
---------------------

Now we can read data from the API using the functions we defined before. We can
get the data from the API and transform it into a pandas DataFrame. We can define
a custom function in order to call the API with different parameters:

.. code-block:: python

   def get_smarter_datasets(params={}):
      url = urljoin(base_url, "smarter-api/datasets")
      results = get_smarter_data(url, params)
      if not results:
         print("No results found")
         return None
      return pd.json_normalize(results)

By calling the function ``get_smarter_datasets`` we can get the data from the API
and transform it into a pandas DataFrame to collect all the *datasets* object from
the *Dataset* endpoint. Similarly, we can define a function to get the data from the
*Breed* endpoint:

.. code-block:: python

   def get_smarter_breeds(params={}):
      url = urljoin(base_url, "smarter-api/breeds")
      results = get_smarter_data(url, params)
      if not results:
         print("No results found")
         return None
      return pd.json_normalize(results)

``get_smarter_breeds`` and ``get_smarter_datasets`` functions can be used to return
all the SMARTER *datasets* and *breeds*. However you can pass additional parameters to
the endpoint using the ``params`` parameter (which can be a dictionary or a list
of tuples, when specifying the same parameter multiple times). For
example, you could retrieve all goats breeds using the ``species`` option:

.. code-block:: python

   goat_breeds = get_smarter_breeds(params={'species': 'Goat'})

Here's another example on how to get the *foreground genotypes* from the *Dataset*
endpoint using the functions we defined before: here we are passing a list of tuples
to the function since the parameter ``type`` is required for both terms and you
cannot define a python *dict* with the same key multiple times:

.. code-block:: python

   foreground_genotypes = get_smarter_datasets(
      params=[('type', 'genotypes'), ('type', 'foreground')])

To have a full list of the available parameters for all the available endpoints
you can check the API documentation at `<https://webserver.ibba.cnr.it/smarter-api/docs>`_.
Let's define another function that could be used for sheep and goat samples
endpoints relying on parameters, and then do a simple query relying on ``species``
and ``breed_code`` parameters:

.. code-block:: python

   def get_smarter_samples(species, params={}):
      # mind that species is lowercase in endpoint url
      species = species.lower()
      url = urljoin(base_url, f"smarter-api/samples/{species}")
      results = get_smarter_data(url, params)
      if not results:
         print("No results found")
         return None
      return pd.json_normalize(results)

   goat_landrace = get_smarter_samples(
      "Goat", params={'breed_code': "LNR"})

We can refine the query by adding more parameters to the query. For example, we
can get the goat samples which have a locations (GPS coordinates) and phenotypes
defined (mind to the double ``_`` in ``locations__exists`` and
``phenotype__exists``):

.. code-block:: python

   goat_landrace = get_smarter_samples(
      "Goat",
      params={
         'breed_code': "LNR",
         'locations__exists': True,
         'phenotype__exists': True}
   )

from the results dataframe, we can extract the ``smarter_id`` and ``breed_code`` columns,
to have a list of our samples in order to subset the full genotype file using ``plink``:

.. code-block:: python

   samples = goat_landrace[['smarter_id', 'breed_code']]
   samples.to_csv("samples.csv", index=False)

Here's another example that could be applied in order to get information on
variants. In this case we will select the goat variants on chromosome
*1* within *1-1000000* positions in *ARS1* assembly:

.. code-block:: python

   def get_smarter_variations(species, assembly, params = {}):
      # mind that species is lowercase in endpoint url, while assembly is uppercase
      species = species.lower()
      assembly = assembly.upper()

      url = urljoin(base_url, f"smarter-api/variants/{species}/{assembly}")
      results = get_smarter_data(url, params)
      if not results:
         print("No results found")
         return None
      return pd.json_normalize(results)

   selected_goat_variations = get_smarter_variations(
      species = "Goat",
      assembly = "ARS1",
      params = {
         "size": 100,
         "region": "1:1-1000000"
      }
   )

.. hint::

   We are planning to simplify the variants response by returning a SNP list of
   the selected SNPs only, in order to be used when subsetting a genotype file
   using plink

.. warning::

   Be careful when using the variants endpoints: getting all the variants will
   takes a lot of time and could fill all your available memory. Avoid to request
   all variants in your R session, unless you know what you are doing
