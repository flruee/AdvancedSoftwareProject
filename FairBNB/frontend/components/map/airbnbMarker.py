from kivy_garden.mapview import MapMarkerPopup
from ...listingDetail import listing_detail
from kivy.app import App

class AirbnbMarker(MapMarkerPopup):
    """
    This class expands MapMarkerPopup
    It displays a marker for a given latitude, longitude and source file.

    Parameters
    ----------
    id_listing : int
        id of a listing
    lon : float
        longitude of listing
    lat : float
        latitude of listing
    source : str
        path to source file used to display marker
    """
    def __init__(self, id_listing, lon, lat, source):
        super(MapMarkerPopup, self).__init__(lon=lon, lat=lat, source=source)
        self.lon=lon
        self.id_listing = id_listing

    def on_release(self):
        """
        If marker is clicked a popup with additional information is opened and  marker turns blue
        """
        app = App.get_running_app()
        app.root.ids.mapview.selected_id=self.id_listing
        self.source= "frontend/icons/marker2.png"
        popup = listing_detail(self.id_listing,self)
        popup.open()

    def reset_marker(self, *args):
        """
        resets marker back to default image

        Parameters
        ----------
        *args
        """
        self.source = "atlas://frontend/icons/frontendAtlas/marker"
        app=App.get_running_app()
        app.root.ids.mapview.selected_id=None
