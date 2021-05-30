from kivy_garden.mapview.clustered_marker_layer import ClusterMapMarker
from kivy.uix.button import ButtonBehavior


class CustomCluster(ClusterMapMarker, ButtonBehavior):
    """
    This class expands the ClusterMapMarker.
    since in the original implementation there was no way to change the source file, we created
    this class for the only purpose of adding a source file.
    """
    def __init__(self, *args, **kwargs):
        super(CustomCluster, self).__init__(source="atlas://frontend/icons/frontendAtlas/cluster", *args, **kwargs)
