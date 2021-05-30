# Fairbnb

This folder holds the FairBNB application.  
`frontend/` holds the code used for the frontend  
`kivymd/` holds kivy specific dependencies.  
`restAPIConnection/` holds the code for the stand-alone class used to communicate with the REST API.  
`main.py` is used to start the application.

## Quickstart
### Python
* use `pip install -r requirements.txt` for the dependencies
* use `python main.py start` to start the application. or `python main.py test` to execute the test.

### Docker (UNIX only)
* build the application with `docker build -t FairBNB`
* run the application with `sudo docker run -it --expose PORT -e DISPLAY=$DISPLAY --user 1000 --network="host" FairBNB`, where `PORT` is the port 
where the REST API runs (if the rest api runs on another computer omit it).
 
## How to use our FairBNB desktop app   

Once you run the app, you will see the **form** page which is our home screen.   
On the top-left corner, there is a hamburger button where you can go through all the screens (form, wish list and map) in our app.   
   
<img width="800" alt="home" src="https://user-images.githubusercontent.com/40763359/120100812-0d988100-c143-11eb-9a00-ff8f490a46b5.png">   
   
<img width="800" alt="hamburger" src="https://user-images.githubusercontent.com/40763359/120100810-0cffea80-c143-11eb-89f2-3204c3158e6e.png">   

Search form takes several inputs to find your best accomodation - neighborhood, guests, age, high rating, super host, fair filter, interests and price.   

* `Neighborhood` You can choose a borough : Bronx, Brooklyn, Manhanttan, Queens and Staten Island.   
* `Guest` You can fill in the number of guests from 1 to 16. This form can be empty if you travel alone.   
* `Age` You can choose your age groups : 18-30, 31-50 and 50+   
* `High rating` You can check the box if you want to see the listings which has more than 4 starts rating.   
* `Super host` You can check the box if you want to see the listings from super host.   
* `Fair filter` You can chexk the box if you want to see the listing which is rented legally. By the law of NYC, the host can not rent more than one listing so we filtered out the listings that is rented out from same hosts.   
* `Interests` You can choose multiple interests that you are looking for during your stays. We pre-assigned specific interests to certain neighborhood and based on this, listings will be returned.   
* `Price` You can set the range of your budget with slider. If you want to set it precisely, you can manually type the price in the fill-in form as well.   
   
After fill in the search form and click the search button, it will bring you to **map** page, where you can see the result of listings that fits to you.    
You can zoom-in and out throug the map to see more/less specific accomodation. You will see the clusters of listing untill you reach the one specific accomodation. When you see the red marker on the map, you can click it then deatil information will pop up. There, you can click the heart icon to add it to the wish list, or you can click magnifier icon which will take you to the airbnb web page of that listing.   
     
<img width="800" alt="map" src="https://user-images.githubusercontent.com/40763359/120100815-0d988100-c143-11eb-87ba-e3902917638c.png">    
   
<img width="800" alt="popup" src="https://user-images.githubusercontent.com/40763359/120100816-0e311780-c143-11eb-84ca-f6377f989508.png">   
    

Once you are done with selecting accomodations, you can go to **wish list** menu and see the comparison of listings that you chose.    
We added labels - "best rating" and "best price" that can make your decision easy and quick.  
   
<img width="800" alt="wishlist" src="https://user-images.githubusercontent.com/40763359/120100811-0cffea80-c143-11eb-88f9-a4e236866986.png">
     
     
Then, enjoy your trip with fairBnB !!! 
    
## Additional Options
In the options.json file one can modify the following options:
* `rest_api_url`: sets the url for the used rest api. Default = "http:/localhost:8888"
* `listing_limit`: The maximum amount of listings to render, decrease if performance is unsatisfactory. Default = 10000
   
 

