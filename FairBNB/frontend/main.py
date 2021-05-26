from kivy.app import App
from kivy.loader import Loader
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.imagelist import SmartTileWithLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from .components.ListingSaveButton import ListingSaveButton
from .listingDetail import RoundedCornerLayout
from .components.filtering.filterMenu import FilterMenu
from .components.form.form import Form
import json
import requests
import os
from .airbnbmapview import AirbnbMapView
from restAPIConnection.restAPIConnection import RestAPIConnection
from frontend.components.compare.compareScreen import CompareScreen


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
    api = RestAPIConnection()

    def on_start(self):
        """
        called on start, inits form
        """
        #todo: delete fps_monitor
        self.fps_monitor_start()
        form = self.root.ids.form
        form.on_start()
        
    def build(self):
        """
        changes loading gif for asyncimage, changes color palette and builds main structure of application
        """
        Loader.loading_image = 'loading.gif'
        self.theme_cls.primary_palette = "DeepOrange"
        self.theme_cls.font_styles["JetBrainsMono"] = [
            "JetBrainsMono",
            16,
            False,
            0.15,
        ]

   # todo: move to different file (show confirmation, grab text, close/show filter dialog, load results)
    def show_confirmation_dialog(self):
        """
        defines content of searchpopupmenu and action of each button
        """
        if not self.dialog:
            self.dialog = MDDialog(
                title="Search:",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color, on_release=self.close_dialog
                    ),
                    MDFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color, on_release=self.grab_text
                    ),
                ],
            )
        self.dialog.get_normal_height()
        self.dialog.open()

    def grab_text(self, inst):
        """
        takes userinput and centers the mapview on defined location
        """
        for obj in self.dialog.content_cls.children:
            if isinstance(obj, MDTextField):
                query = obj.text
                query += ' NY United States'
                response = requests.get("http://localhost:8888/search_address",params={'location':query})
                app = App.get_running_app()
                mapview = app.root.ids.mapview
                locations = json.loads(response.text)
                print(locations)
                mapview.center_on(locations['lat'], locations['lng'])
        self.dialog.dismiss()

    def close_dialog(self, inst):
        """
        close searchpopupmenu
        """
        self.dialog.dismiss()

    def show_filter_dialog(self):
        """
        open filtermenu
        """
        if not self.dialog:
            self.dialog = MDDialog(

            )

    def load_results(self):
        path = 'bookmarks'

        full_path = os.path.join(os.getcwd(), path)
        for filenames in os.walk(full_path):
            for filename in filenames[2]:
                current_file = open(os.path.join(full_path, filename), "r")
                data = json.load(current_file)

                superbox = SmartTileWithLabel(
                    size_hint_y= None,
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

