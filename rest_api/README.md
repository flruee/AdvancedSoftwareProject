# REST API

This is the REST API.

## Quickstart

* Install all modules via `npm install`
* Build Database
  * via the setupDB folder
    * Change to the setupDB folder.
    * Create a folder *data*
    * <strike>Download~ the datasets from [here](http://data.insideairbnb.com/united-states/ny/new-york-city/2019-07-08/data/listings.csv.gz)
and [here](http://data.insideairbnb.com/united-states/ny/new-york-city/2019-07-08/data/reviews.csv.gz) and put them into *data*</strike><br/>It seems the website stopped hosting the datasets, so the data is already provided in 'setupDB/data'.
    * run questionairedictionnary.py
    * Modify the top of the setupDB.py file with your postgres credentials
    * run setupDB.py
  * via the db folder
    * Go to the *db* folder
    * Execute assembleDump.py
    * import the resulting file 'pg_dump.sql' into your database
* Create a file '.env' in the rest_api folder as follows:
```
PORT = //The port the rest api will listen to
DB_HOST = //The ip of the host, can also put localhost here
DB_USER = //your db username
DB_PASSWORD = //db username password
DB_NAME = //the db name
DB_PORT= //the port the db listens to (default: 5432)
```
* use `npm start` to start the api or `npm test` to execute all tests in '/test'

## Further information
For further information look at the [wiki page](https://github.com/flruee/AdvancedSoftwareProject/wiki/Rest-API).
