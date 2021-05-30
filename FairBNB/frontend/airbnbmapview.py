from kivy_garden.mapview import MapView
from kivy.app import App
from .components.map.airbnbMarker import AirbnbMarker
from .components.map.customCluster import CustomCluster
from .mapViewOverride.clustered_marker_layer import ClusteredMarkerLayer
import json

class AirbnbMapView(MapView):
    """
    This Class holds and displays the Map
    """
    listing_id_list = []
    firstCall = True
    selected_id = -1
    def __init__(self, *args, **kwargs):
        super(AirbnbMapView, self).__init__(*args, **kwargs)
        with open("options.json") as f:
            options = json.loads(f.read())
            self.limit = options['listing_limit']

    def get_airbnb_in_fov(self, *args):
        """
        query api for listings in fov. Fov defined by 4 corners of screen. places Clustermarkers & Markers wherever
        there is a matching listing in our database.
        """
        # If we switch from another screen onto the map screen the longitude and latitude are too small
        # The map screen is probably minimized in the background somewhere which causes the problem
        # If we increase the latitude and longitude range the problem is fixed
        if len(args) > 0 and args[0] == "on_enter":
            self.firstCall = True
        lat1, lon1, lat2, lon2 = self.get_bbox()
        if self.firstCall:
            lat1 += (lat1-lat2)*2
            lat2 -= (lat1-lat2)*2
            lon1 += (lon1-lon2)*2
            lon2 -= (lon1-lon2)*2
            self.firstCall = False

        app = App.get_running_app()
        custom_filter = {'latitude.ge': lat1, 'latitude.le': lat2, 'longitude.ge': lon1, 'longitude.le': lon2}
        
        # seems to be more efficient to exploit the pointer ability of list elements
        listings = [None]
        app.api.get_listing_location(listings, custom_filter)

        layer = ClusteredMarkerLayer(cluster_cls=CustomCluster, cluster_radius="200dp", cluster_max_zoom=18)
        cnt = 0
        # add listing to layer, break after 10'000 listings for performance reasons
        for listing in listings[0]:
            if cnt >= self.limit:
                break
            listing_id = listing['id']
            if listing_id in self.listing_id_list:
                continue
            else:
                #Display selected id as a blue marker
                if(listing_id==self.selected_id):
                    layer.add_marker(
                    lon=float(listing['longitude']),
                    lat=float(listing['latitude']),
                    cls=AirbnbMarker,
                    options={
                        "source": "frontend/icons/marker2.png",
                        "id_listing": listing['id']
                    }
                )
                # Display normal listings with red marker
                else:
                    layer.add_marker(
                        lon=float(listing['longitude']),
                        lat=float(listing['latitude']),
                        cls=AirbnbMarker,
                        options={
                            "source": "atlas://frontend/icons/frontendAtlas/marker",
                            "id_listing": listing['id']
                        }
                    )
            cnt += 1
        # remove old layers
        for child in self.children:
            if isinstance(child, ClusteredMarkerLayer):
                self.remove_widget(child)
        # add layer to map
        self.add_widget(layer)
