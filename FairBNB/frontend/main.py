from kivy.loader import Loader
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.imagelist import SmartTileWithLabel
from .components.ListingSaveButton import ListingSaveButton
from .listingDetail import RoundedCornerLayout
from .components.filtering.filterMenu import FilterMenu
from .components.form.form import Form
import json
import os
from .airbnbmapview import AirbnbMapView
from restAPIConnection.restAPIConnection import RestAPIConnection
from frontend.components.compare.compareScreen import CompareScreen
from kivy.core.window import Window
Window.maximize()

class ContentNavigationDrawer(BoxLayout):
    """
    required for .kv files
    """
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class Content(BoxLayout):
    """
    required for .kv file
    """
    pass


# Todo: delete?
class BaseWidget(MDFloatLayout):
    pass


class MainApp(MDApp):
    """
    MainApp: builds application by reading main.kv file
    """
    dialog = None
    search_menu = None
    with open("options.json") as f:
        options = json.loads(f.read())
    print(options)
    api = RestAPIConnection(base_url=options["rest_api_url"])

    def on_start(self):
        """
        called on start, inits form
        """
        form = self.root.ids.form
        form.on_start()
        
    def build(self):
        """
        changes loading gif for asyncimage, changes color palette and builds main structure of application
        """
        Loader.loading_image = 'frontend/icons/loading.gif'
        self.theme_cls.primary_palette = "DeepOrange"
        self.theme_cls.font_styles["JetBrainsMono"] = [
            "JetBrainsMono",
            16,
            False,
            0.15,
        ]

    def load_results(self):
        path = 'bookmarks'

        full_path = os.path.join(os.getcwd(), path)
        for filenames in os.walk(full_path):
            for filename in filenames[2]:
                current_file = open(os.path.join(full_path, filename), "r")
                data = json.load(current_file)

                superbox = SmartTileWithLabel(
                    size_hint_y=None,
                    height="240dp",
                    source=data['picture_url'],
                    text=f"Price: {data['price']}$/night"
                         f"\nRoomType: {data['room_type']}"
                         f"\nBorough: {data['neighbourhood_group_cleansed']}"

                )
                bookmarkbutton = ListingSaveButton(data)
                superbox.add_widget(bookmarkbutton)
                self.root.ids.imagelist.add_widget(superbox)


def run():
    MainApp().run()


if __name__ == '__main__':
    run()
