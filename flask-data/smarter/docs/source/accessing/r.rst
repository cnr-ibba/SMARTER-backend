
Accessing data using R
======================

.. toctree::
   :maxdepth: 4

Here are some examples on how to interact with SMARTER-backend API using ``R``. 
You will need to set up some utility functions in order to save your time by avoiding
repeating stuff

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

``base_url`` we will set this variable for simplicity in order to make all our 
request to the same server. Next, we define the ``get_smarter_token`` function
which require user and password as parameters. The ``readline`` and ``getPass::getPass``
default values are not strictly required, we use them in order to not write our 
credentials in our code: the function will prompt for those values if not provided 
during function call. The token string is parsed and written into ``token`` variable.

.. hint:: 

   Rstudio has a dedicated section on `Securing Credentials <https://db.rstudio.com/best-practices/managing-credentials/>`_.
   We recommend to follow their guidelines.
   
Deal with data and pagination
-----------------------------

Next, before starting query SMARTER-backend, we can define some utility function 
(as suggested by `Best practices for API packages <https://cran.r-project.org/web/packages/httr/vignettes/api-packages.html>`_)
in order to deal with pagination and API errors. We will read our data with 
``jsonlite`` package in order to **flatten** our results (read nested object and 
add them as a column in the resulting dataframe):

.. code-block:: r

   read_url <- function(url, token, query = list()) {
      # getting the required url
      resp <-
         GET(url, query = query, add_headers(Authorization = paste("Bearer", token)))

      # check errors
      if (http_type(resp) != "application/json") {
         stop("API did not return json", call. = FALSE)
      }

      # parse a JSON response. fromJSON to flatten results
      parsed <-
         jsonlite::fromJSON(content(resp, "text", encoding = "utf-8"), flatten =
                              TRUE)

      # deal with API errors
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
      # read and parse url
      parsed <- read_url(url, token, query)

      # track results in df
      results <- parsed$items

      # check for pagination
      while (!is.null(parsed$`next`)) {
         # append next value to base url
         next_url <- httr::modify_url(base_url, path = parsed$`next`)

         # query arguments are already in url
         parsed <- read_url(next_url, token)

         # append new results to df
         results <- dplyr::bind_rows(results, parsed$items)
      }

      # return an S3 obj (with last values read)
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
the desidered endpoint. This function will call the function we defined before
and will return all the results in a *dataframe*. For example, to deal with the 
Breed endpoint: 

.. code-block:: r

   get_smarter_breeds <- function(token, query = list()) {
      url <- httr::modify_url(base_url, path = "/smarter-api/breeds")
      data <- get_smarter_data(url, token, query)
      results <- data$results
      return(results)
   }

   goat_breeds <-
      get_smarter_breeds(token, query = list(species = "Goat"))

the ``get_smarter_breeds`` will be a generic function able to return all the SMARTER 
breed. If you want to select only the *Goat* breed, we can specify ``species = "Goat"``
as the ``query`` parameters. If you need to filter using another parameters, for 
example for searcing the *land* term as in the :ref:`Query parameters` example,
you will call the same function by passing a new parameter:

.. code-block:: r 

   search_goat_breeds <- 
      get_smarter_breeds(token, query = list(
         species = "Goat", search = "land")
      )
      
``search_goat_breeds`` will be a dataframe with the same results of the query URL::
   
   https://webserver.ibba.cnr.it/smarter-api/breeds?species=Goat&search=land
