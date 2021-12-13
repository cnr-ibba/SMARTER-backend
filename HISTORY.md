
History
=======

TODO
----

* support for GIS search in sample endpoints [#13](https://github.com/cnr-ibba/SMARTER-backend/issues/13)
* configure MongoDB memory usage [#12](https://github.com/cnr-ibba/SMARTER-backend/issues/12)
* configure logging [#7](https://github.com/cnr-ibba/SMARTER-backend/issues/7)

0.2.0.dev0
----------

* move base location from /api/ to /smarter-api/
* document API with `flasgger` [#6](https://github.com/cnr-ibba/SMARTER-backend/issues/6)
* add endpoint for supported assemblies variants [#11](https://github.com/cnr-ibba/SMARTER-backend/issues/11)
* add info endpoint
* query with multiple parameters [#23](https://github.com/cnr-ibba/SMARTER-backend/issues/23)
* return 4xx error when querying with wrong parameters [#22](https://github.com/cnr-ibba/SMARTER-backend/issues/22)
* Support `type` argument when searching samples
* Track version with bump2version

0.1.0 (2021-11-11)
------------------

* First release of SMARTER-backend
* Support user authentication through JWT
* Start documentation with readthedocs
* Add endpoints for the principal features
  * breeds
  * supported chips
  * datasets
  * samples
  * variants
