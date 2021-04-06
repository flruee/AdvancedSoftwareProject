from kivy_garden.mapview import MapView
from kivy.clock import Clock
from kivy.app import App
import requests
import json
from airbnbmarker import AirbnbMarker


class AirbnbMapView(MapView):
    getting_airbnb_timer = None
    listing_id_list = []

    def start_getting_airbnb_in_fov(self):
        # After one second, get listings in field of view
        try:
            self.getting_airbnb_timer.cancel()
        except:
            pass

        self.getting_airbnb_timer = Clock.schedule_once(self.get_airbnb_in_fov, 1)

    def get_airbnb_in_fov(self, *args):
        app = App.get_running_app()
        lat1, lon1, lat2, lon2 = self.get_bbox()
        data = requests.get(f"http://localhost:8888/listings/location?lat1={lat1}&lat2={lat2}&lon1={lon1}&lon2={lon2}")
        listings = json.loads(data.text)
        for listing in listings:
            id = listing['id']
            if id in self.listing_id_list:
                continue
            else:
                self.add_listing(listing)

    def add_listing(self, listing):
        # create marker
        lat = listing['latitude']
        lon = listing['longitude']
        marker = AirbnbMarker(lat=lat, lon=lon, source='marker.png')
        marker.listing_data = listing

        # add marker to map
        self.add_widget(marker)

        # keep track of markers id (avoid adding marker twice and keep it onscreen)
        id = listing['id']
        self.listing_id_list.append(id)