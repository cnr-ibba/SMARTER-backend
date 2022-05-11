
History
=======

TODO
----

* Configure logging [#7](https://github.com/cnr-ibba/SMARTER-backend/issues/7)
* Try to compress responses [#34](https://github.com/cnr-ibba/SMARTER-backend/issues/34)
* Support searching with patterns on original and smarter id [#19](https://github.com/cnr-ibba/SMARTER-backend/issues/19)
* Support `text/csv` header request [#16](https://github.com/cnr-ibba/SMARTER-backend/issues/16)
* Substitute flask-restful components with better alternatives [#10](https://github.com/cnr-ibba/SMARTER-backend/issues/10)

0.2.1 (2022-05-11)
------------------

* Fix `dataset` parameter in swagger Samples endpoint
* Add country endpoint [#33](https://github.com/cnr-ibba/SMARTER-backend/issues/33)
* Support multiple parameters in Breeds endpoint [#29](https://github.com/cnr-ibba/SMARTER-backend/issues/29)
* Support parameters into GeoJSON endpoint [#32](https://github.com/cnr-ibba/SMARTER-backend/issues/32)
* Return error when searching variant with a wrong region [#30](https://github.com/cnr-ibba/SMARTER-backend/issues/30)

0.2.0 (2021-12-20)
------------------

* support for GIS search in sample endpoints [#13](https://github.com/cnr-ibba/SMARTER-backend/issues/13)
  * document *GeoJSON* endpoint and GIS parameters using swagger
  * returning all samples as *GeoJSON* FeatureCollection
  * select samples within a sphere
  * select samples inside a polygon
  * model locations with `MultiPointField`
* configure MongoDB memory usage [#12](https://github.com/cnr-ibba/SMARTER-backend/issues/12)
* move base location from `/api/` to `/smarter-api/`
* document API with `flasgger` [#6](https://github.com/cnr-ibba/SMARTER-backend/issues/6)
* add endpoint for supported assemblies variants [#11](https://github.com/cnr-ibba/SMARTER-backend/issues/11)
* add info endpoint
* query with multiple parameters [#23](https://github.com/cnr-ibba/SMARTER-backend/issues/23)
* return 4xx error when querying with wrong parameters [#22](https://github.com/cnr-ibba/SMARTER-backend/issues/22)
* Support `type` argument when searching samples
* Track version with `bump2version`

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
