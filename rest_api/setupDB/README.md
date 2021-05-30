scripts loads data from data folder and puts it into postgres

since files are too large you have to download them yourself from the following links
listings:    
http://data.insideairbnb.com/united-states/ny/new-york-city/2019-07-08/data/listings.csv.gz
full text reviews:  
http://data.insideairbnb.com/united-states/ny/new-york-city/2019-07-08/data/reviews.csv.gz  
NOTE: It seems the above files are not hosted anymore. We added those in the data folder you'll have to decompress them.  

for the script you need pandas,sqlalchemy and psycopg2.
if psycopg2 fails to install try psycopg2-binary 
