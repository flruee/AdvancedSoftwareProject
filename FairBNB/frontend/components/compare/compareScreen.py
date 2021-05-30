import os
import webbrowser
import json
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivymd.uix.card import MDSeparator
from kivymd.uix.chip import MDChip
from kivymd.uix.button import MDIconButton
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.boxlayout import MDBoxLayout
from frontend.components.ListingSaveButton import ListingSaveButton


class WebButton(MDIconButton):
    """
    Class defined in order to dynamically define the on_press functionality

    Parameters
    ----------
    url_dictionary : dict
    """
    def __init__(self, *args, url_dictionary=None, **kwargs):
        super(MDIconButton, self).__init__(*args, **kwargs)
        self.url_dictionary = url_dictionary

    def on_press(self):
        webbrowser.open(self.url_dictionary[self])


class LocationButton(MDIconButton):
    """
    Class defined in order to dynamically define the on_press functionality

    Parameters
    ----------
    location_dictionary : dict
    """
    def __init__(self, *args, location_dictionary=None,listing_id, **kwargs):
        super(MDIconButton, self).__init__(*args, **kwargs)
        self.location_dictionary = location_dictionary
        self.listing_id = listing_id

    def on_press(self):
        """
        takes lat,long and switches to mapscreen focused on given coordinates
        """
        print("on_press")
        app = App.get_running_app()
        mapview = app.root.ids.mapview
        mapview.zoom = 19
        mapview.center_on(self.location_dictionary[self][0], self.location_dictionary[self][1])
        screen_manager = app.root.ids['screen_manager']
        screen_manager.current = "mapscreen"
        mapview.selected_id = self.listing_id
        print(self.listing_id)
        print(mapview.selected_id)


class ContentReviews(MDBoxLayout):
    """
    required for .kv file
    """
    pass


class CompareScreen(MDBoxLayout):
    """
    This Screen is designed to compare the listings saved to wishlist. It consists of boxlayouts, one for each listing
    """

    def remove_wishlist_superboxes(self):
        """
        This function removes all the widgets added to the comparescreen. This is necessary since on entry all listings
        stored in json file will be added to comparescreen - ultimately avoiding duplicates.
        """
        children = self.ids.comparebox.children
        children_copy = children.copy()
        for child in children_copy:
            self.ids.comparebox.remove_widget(child)

    def load_bookmarked(self):
        """
        This function reads the json's stored in /bookmarks. It then proceeds to initialize the widgets for each listing
        It adds all the widget to the boxlayout. Finally, it checks which listing has the lowest price/highest rating
        and add tags accordingly. The lowest price cannot be 0 and the best rated listing must have at least 10 ratings.
        """
        best_price_box = {}
        best_rating_box = {}
        web_button_data = {}
        location_data = {}
        path = 'bookmarks'
        full_path = os.path.join(os.getcwd(), path)
        for filenames in os.walk(full_path):
            for filename in filenames[2]:
                current_file = open(os.path.join(full_path, filename), "r")
                data = json.load(current_file)
                main_box_per_listing = MDBoxLayout(
                    size_hint_y=None,
                    height="240dp",
                    orientation="horizontal",
                    padding=[dp(4), dp(4)],
                    spacing=dp(4)
                )
                image_box = MDFloatLayout(
                    size_hint=[0.4, 1]
                )
                text_box = MDBoxLayout(
                    orientation='horizontal'
                )
                super_vertical_box = MDBoxLayout(
                    orientation='vertical',
                )
                super_horizontal_box = MDBoxLayout(
                    orientation='horizontal',
                    padding=dp(10)
                )
                vertical_box_tile_and_room_type = MDBoxLayout(
                    orientation='vertical',
                    size_hint_y=0.7
                )
                vertical_box_room_type = MDBoxLayout(
                    size_hint_y=0.3
                )
                vertical_box_title = MDBoxLayout(
                    size_hint_y=0.7
                )
                vertical_box_buttons = MDFloatLayout(
                    size_hint_x=0.1
                )
                vertical_box_nr_of_guests = MDBoxLayout(
                    orientation='horizontal'
                )
                horizontal_box_rating = MDBoxLayout(
                    orientation='horizontal'
                )
                horizontal_box_star = MDBoxLayout(
                    orientation='horizontal',
                    size_hint_x=0.3
                )
                img = AsyncImage(source=data['picture_url'], allow_stretch=True, keep_ratio=False,
                                 pos_hint={'center_x': .5, 'center_y': .5},
                                 size_hint_y=1, width=100)

                roomtype_label = MDLabel(text=f"[color=808080]{data['room_type']} in {data['village']}"
                                              f" ({data['borough']})[/color]",
                                         markup=True,
                                         halign='left',
                                         pos_hint={'center_x': .5, 'center_y': .75})

                title_label = MDLabel(text=f"[size=25]{data['name']}[/size]",
                                      markup=True,
                                      halign='left',
                                      pos_hint={'center_x': .5, 'center_y': .85})
                """
                reviews_expansion = MDExpansionPanel(
                                        icon="",  # panel icon
                                        content=ContentReviews(),  # panel content
                                        panel_cls=MDExpansionPanelOneLine(text="Reviews"),  # panel class
                )
                """
                if data['guests_included'] == 1:

                    guest_text = f"{data['guests_included']} guest · {data['minimum_nights']} minimum nights · " \
                                 f"{data['maximum_nights']} maximum nights"
                else:
                    guest_text = f"{data['guests_included']} guests · {data['minimum_nights']} minimum nights · " \
                                 f"{data['maximum_nights']} maximum nights"

                guests_included_label = MDLabel(
                    text=guest_text,
                    halign='left',
                    pos_hint={'center_x': .5, 'center_y': .35}
                )

                price_label = MDLabel(text=f"[size=35][b]{data['price']}$[/b]/night[/size]",
                                      markup=True,
                                      halign='right',
                                      pos_hint={'center_x': 0.3, 'center_y': .1})

                line = MDSeparator(height=dp(1))

                if not data['price'] == 0:
                    best_price_box[image_box] = data['price']
                if data['number_of_reviews'] >= 10:
                    best_rating_box[image_box] = float(data['review_score'])/20

                superhost_chip = MDChip(
                    text='SUPERHOST',
                    pos_hint={'center_x': .20, 'center_y': .90},
                    icon='',
                    color=[1, 1, 1, 1],
                )

                staricon = MDIcon(
                    icon='star',
                    pos_hint={'left_x': .50, 'center_y': .08}
                )
                starlabel = MDLabel(
                    text=f"[b]{float(data['review_score']) / 20}[/b] ({data['number_of_reviews']})", markup=True,
                    pos_hint={'left_x': .50, 'center_y': .07}
                )
                webbutton = WebButton(
                    icon='search-web',
                    user_font_size="36sp",
                    pos_hint={'center_x': .9, 'center_y': .3},
                    url_dictionary=web_button_data
                )
                web_button_data[webbutton] = data['listing_url']

                bookmarkbutton = ListingSaveButton(
                    data,
                    pos_hint={'center_x': .9, 'center_y': .7},
                    opposite_colors=False,
                    icon='delete'
                )
                loc_button = LocationButton(
                    icon='map-outline',
                    pos_hint={'center_x': .9, 'center_y': .5},
                    location_dictionary=location_data,
                    listing_id=data['id']
                )
                location_data[loc_button] = [float(data['latitude']), float(data['longitude'])]

                # ADD WIDGETS

                image_box.add_widget(img)
                if data['is_superhost']:
                    image_box.add_widget(superhost_chip)

                vertical_box_title.add_widget(title_label)
                vertical_box_room_type.add_widget(roomtype_label)
                vertical_box_tile_and_room_type.add_widget(vertical_box_room_type)
                vertical_box_tile_and_room_type.add_widget(vertical_box_title)
                vertical_box_buttons.add_widget(bookmarkbutton)
                vertical_box_buttons.add_widget(loc_button)
                vertical_box_buttons.add_widget(webbutton)

                horizontal_box_star.add_widget(staricon)
                horizontal_box_star.add_widget(starlabel)
                horizontal_box_rating.add_widget(horizontal_box_star)
                horizontal_box_rating.add_widget(price_label)
                super_horizontal_box.add_widget(horizontal_box_rating)

                vertical_box_nr_of_guests.add_widget(guests_included_label)
                #vertical_box_nr_of_guests.add_widget(reviews_expansion)

                super_vertical_box.add_widget(vertical_box_tile_and_room_type)
                super_vertical_box.add_widget(vertical_box_nr_of_guests)
                super_vertical_box.add_widget(super_horizontal_box)

                text_box.add_widget(super_vertical_box)
                text_box.add_widget(vertical_box_buttons)

                main_box_per_listing.add_widget(image_box)
                main_box_per_listing.add_widget(text_box)
                self.ids.comparebox.add_widget(main_box_per_listing)
                self.ids.comparebox.add_widget(line)

        best_price_chip = MDChip(
            text='BEST PRICE',
            pos_hint={'center_x': .8, 'center_y': .9},
            icon='',
            text_color=[1, 1, 1, 1],
            color=[0.01, 0.28, 0.99, 1],
            spacing=dp(4)
        )
        #if no listing is bookmarked then return
        print(len(self.ids.comparebox.children))
        if(len(self.ids.comparebox.children)==0):
            empty_label = MDLabel(text="No listing on Wishlist.\nPlease add some listings on the Map screen",pos_hint={"center_x":0.9,"center_y":4})
            self.ids.comparebox.height = self.height
            self.ids.comparebox.add_widget(empty_label)
        elif(len(self.ids.comparebox.children)<=2):
            return
        else:        
            min(best_price_box, key=best_price_box.get).add_widget(best_price_chip)
            if min(best_price_box, key=best_price_box.get) == max(best_rating_box, key=best_rating_box.get):
                pos = {'center_x': .8, 'center_y': 0.77}
            else:
                pos = {'center_x': .8, 'center_y': .9}
            best_rating_chip = MDChip(
                text='BEST RATING',
                pos_hint=pos,
                icon='',
                color=[0.98, 0.92, 0.01, 1],
                spacing=dp(4)
            )
            # needs 10 ratings
            if len(best_rating_box) is not 0:
                max(best_rating_box, key=best_rating_box.get).add_widget(best_rating_chip)


