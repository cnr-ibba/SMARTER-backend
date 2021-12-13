
Accessing data using R
======================

.. toctree::
   :maxdepth: 4

Here are some examples on how to interact with SMARTER-backend API using ``R``. 
You will need to set up some utility functions in order to save your time by avoiding
repeating stuff.

Importing R libraries
---------------------

First of all, let's start with importing some ``R`` libraries (maybe you will need
to install some of them first):

.. code-block:: r

   library(httr)
   library(jsonlite)
   library(getPass)
   library(dplyr)

``httr`` is required to send requests and get response from SMARTER-backend API;
``jsonlite`` is required to parse ``JSON`` output, which is the default format 
of the API response. ``getPass`` is not strictly required, it will prompt for our 
credentials in order to not store them in our code. ``dplyr`` is useful to manage 
dataframes, for examples when they have different columns (like response from
SMARTER-backend)

Generate a JWT token with R
---------------------------

As stated in our :ref:`Authentication` section of this guide, you need to generate 
a :ref:`JWT token <JWT Authentication>` in order to get full access to smarter 
metadata. Here is an utility function to request a token by providing your 
credentials with a ``POST`` HTTP method:

.. code-block:: r

   base_url <- "https://webserver.ibba.cnr.it"

   get_smarter_token <-
      function(username = readline(prompt = "Username ? "),
               password = getPass::getPass("Password ? ")) {
         auth_url <-
            httr::modify_url(base_url, path = "/smarter-api/auth/login")

         resp <-
            POST(
            auth_url,
            body = list(username = username, password = password),
            encode = "json"
            )

         # this will read a JSON by default
         data <- httr::content(resp)

         # returning only the token as a string
         return(data$token)
      }

   token <- get_smarter_token()

``base_url`` is defined for simplicity in order to make all our request to the
same server. The ``get_smarter_token`` function requires *user* and *password* 
as parameters. The ``readline`` and ``getPass::getPass`` functions used as
default values are not strictly required, we use them in order to not write
credentials in our code: the function will prompt for those values if not provided 
during function call. The token string is parsed and written into ``token`` variable:
This is the value we need to add to each requests *header*

.. hint:: 

   Rstudio has a dedicated section on `Securing Credentials <https://db.rstudio.com/best-practices/managing-credentials/>`_.
   We recommend to follow their guidelines.
   
Deal with data and pagination
-----------------------------

Next, before starting query SMARTER-backend, we can define more utility functions
(as suggested by `Best practices for API packages <https://cran.r-project.org/web/packages/httr/vignettes/api-packages.html>`_)
in order to deal with pagination and API errors. We will read our data with 
``jsonlite`` package in order to **flatten** our results (read nested object and 
add them as columns in the resulting dataframe):

.. code-block:: r

   read_url <- function(url, token, query = list()) {
      # in this request, we add the token to the request header section
      resp <-
         GET(url, query = query, add_headers(Authorization = paste("Bearer", token)))

      # check errors: SMARTER-backend is supposed to return JSON objects
      if (http_type(resp) != "application/json") {
         stop("API did not return json", call. = FALSE)
      }

      # parse a JSON response. fromJSON to flatten results
      parsed <-
         jsonlite::fromJSON(
            content(resp, "text", encoding = "utf-8"), 
            flatten = TRUE
         )

      # deal with API errors: not "200 Ok" status
      if (http_error(resp)) {
         stop(
            sprintf(
            "SMARTER API returned an error [%s]: '%s'",
            status_code(resp),
            parsed$message
            ),
            call. = FALSE
         )
      }

      return(parsed)
   }


   get_smarter_data <- function(url, token, query = list()) {
      # do the request and parse data with our function
      parsed <- read_url(url, token, query)

      # track results in df
      results <- parsed$items

      # check for pagination
      while (!is.null(parsed$`next`)) {
         # append next value to base url
         next_url <- httr::modify_url(base_url, path = parsed$`next`)

         # query arguments are already in url: get next page
         parsed <- read_url(next_url, token)

         # append new results to df. Deal with different columns
         results <- dplyr::bind_rows(results, parsed$items)
      }

      # return an S3 obj with the data we got
      structure(list(
         content = parsed,
         url = url,
         results = results
      ),
      class = "smarter_api")
   }


Our functions will take an ``url`` parameter, which will be our API endpoint, the 
``token`` that will be added in the header request as described in :ref:`Authentication`
section of our documentation and ``query``, which will be a list of 
parameters that will enhance our queries as described in :ref:`Query parameters`

Read data with R 
----------------

Next we can try to read data from our API by defining custom functions around 
the desidered endpoint. This function will call the functions previously defined
and will return all the results in a *dataframe*. Here's a sample function to 
deal with datasets objects by querying the *datasets* endpoint:

.. code-block:: r

   get_smarter_datasets <- function(token, query=list()) {
      url <-
         modify_url(base_url, path = "/smarter-api/datasets")

      data <- get_smarter_data(url, token, query)

      # returning only the results dataframe
      data$results
   }

   all_datasets <- get_smarter_datasets(token)

By calling the defined ``get_smarter_datasets`` function and providing a valid
token as parameter you will retrieve all datasets and you will store them in 
the ``all_datasets`` dataframe. Similarly, to deal with the Breed endpoint you could 
define the ``get_smarter_breeds`` function: 

.. code-block:: r

   get_smarter_breeds <- function(token, query = list()) {
      # setting the URL endpoint
      url <- httr::modify_url(base_url, path = "/smarter-api/breeds")

      # reading our data
      data <- get_smarter_data(url, token, query)

      # returning only the results dataframe
      data$results
   }

   goat_breeds <-
      get_smarter_breeds(token, query = list(species = "Goat"))

``get_smarter_breeds`` and ``get_smarter_datasets`` functions can be used to return 
all the SMARTER datasets and breeds. However you can pass additional parameters to 
the endpoint using the ``query`` parameter (which need to be a ``list``). For 
example, you could retrieve all the *genotypes* datasets using the ``type`` parameter:

.. code-block:: r

   genotypes_datasets <- get_smarter_datasets(token, query = list(type="genotypes"))

Since query accepts ``list``, you can specify the same parameter multiple times 
(if the endpoints supports this type of query). For example, if you need only the 
*foreground genotypes*, you can select dataset like this:

.. code-block:: r

   foreground_genotypes_datasets <- get_smarter_datasets(
      token, query = list(type="genotypes", type="foreground"))

You can add other parameters to refine your query, for example
if you want to select only the *Goat* breeds, you can specify 
``species = "Goat"`` in the ``query`` parameter. If you need also to search 
for the *land* term in the *breed* name, you will call the same function 
by adding a new parameter:

.. code-block:: r 

   search_goat_breeds <- 
      get_smarter_breeds(token, query = list(
         species = "Goat", search = "land")
      )
      
``search_goat_breeds`` will be a dataframe with the same results of the query URL::
   
   https://webserver.ibba.cnr.it/smarter-api/breeds?species=Goat&search=land

We can select only the column we need by subsetting dataframe columns, or using 
dplyr `select <https://dplyr.tidyverse.org/reference/select.html>`_:

.. code-block:: r

   search_goat_breeds <- search_goat_breeds %>% select(name, code)

Breed code and names can be used to get from samples from the proper endpoint. 
Let's define another function that could be used for sheep and goat samples 
endpoints relying on parameters:

.. code-block:: r 

   get_smarter_samples <- function(token, species, query = list()) {
      # mind that species is lowercase in endpoint url
      species <- tolower(species)

      url <-
         modify_url(base_url, path = sprintf("/smarter-api/samples/%s", species))

      data <- get_smarter_data(url, token, query)
      
      # returning only the results dataframe
      data$results
   }

   landrace_samples <- get_smarter_samples(
      token,
      species = "Goat",
      query = list(breed_code = "LNR")
   )

As for the breed example, we can refine our query, for example by selecting 
Landrace goat samples which have a locations (GPS coordinates) and phenotypes
defined (mind to the double ``_`` in ``locations__exists`` and 
``phenotype__exists``):

.. code-block:: r

   selected_landrace_samples <- get_smarter_samples(
      token,
      species = "Goat",
      query = list(
         breed_code = "LNR", 
         locations__exists = TRUE,
         phenotype__exists = TRUE)
   )

As before we can select the ``smarter_id`` columns, to have a list of our samples 
in order to subset the full genotype file using ``plink``:

.. code-block:: r

   selected_landrace_samples %>% select(smarter_id)

The same could be applied on variants endpoins in order to get information on
variants. In the following example we will select the goat variants on chromosome 
*1* within *1-1000000* position in *ARS1* assembly:

.. code-block:: r 

   get_smarter_variations <- function(token, species, query = list()) {
      # mind that species is lowercase in endpoint url
      species <- tolower(species)
      assembly <- toupper(assembly)

      url <-
         modify_url(base_url, path = sprintf("/smarter-api/variants/%s/%s", species, assembly))

      data <- get_smarter_data(url, token, query)

      # returning only the results dataframe
      data$results
   }

   selected_goat_variations <- get_smarter_variations(
      token,
      species = "Goat",
      assembly = "ARS1",
      query = list(
         size = 100,
         region = "1:1-1000000"
      )
   )

.. hint:: 

   We are planning to simplify the variants response by returning a SNP list of
   the selected SNPs only, in order to be used when subsetting a genotype file 
   using plink

.. warning:: 

   Be careful when using the variants endpoints: getting all the variants will 
   takes a lot of time and could fill all your available memory. Avoid to request 
   all variants in your R session, unless you know what you are doing
