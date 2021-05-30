from kivy.uix.popup import Popup
from kivy.uix.image import AsyncImage
from kivy.app import App
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.chip import MDChip
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel, MDIcon
from .components.ListingSaveButton import ListingSaveButton
import webbrowser
from kivy.config import Config
from kivy.graphics import Color, RoundedRectangle


class RoundedCornerLayout(MDBoxLayout):
    """
    Customised layout for rounded corners on listing-popup when clicking on marker
    """
    orientation = 'vertical'

    def __init__(self):
        super().__init__()

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[(40, 40), (40, 40), (20, 20), (20, 20)],
            )
        self.bind(pos=lambda obj, pos: setattr(self.rect, "pos", pos))
        self.bind(size=lambda obj, size: setattr(self.rect, "size", size))

        self.size_hint = (None, None)
        self.size = (275, 350)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.background_color = 0, 0, 0, 1


def open_link(url):
    """
    opens the url in browser

    Parameters
    ----------
    url :   str
            The `url` defined in the listing, clicked on by user
    """
    webbrowser.open(url)


def listing_detail(listing_id, parent):
    """
    Fetches listing details when clicking on marker on map. First makes API get request then continues to arrange data
    in widgets which is added to the Mapview Screen as popup.

    Parameters
    ----------
    listing_id : int
    parent : widget

    Returns
    -------
    popup : widget
    """

    # get Data
    custom_filters = {'id.eq': str(listing_id)}
    app = App.get_running_app()
    detail_data = [None]
    other_data = [None]
    location_data = [None]
    review_data = [None]
    app.api.get_listing_detail(detail_data, custom_filters)
    app.api.get_listing_other(other_data, custom_filters)
    app.api.get_listing_location(location_data, custom_filters)
    app.api.get_reviews(review_data, custom_filters)

    # merge data
    data = {**detail_data[0][0], **other_data[0][0], **location_data[0][0]}
    try:
        data = {**data, **review_data[0][0]}
    except IndexError:
        pass
    superbox = RoundedCornerLayout(
    )
    imagebox = MDFloatLayout(
        )
    textbox = MDFloatLayout(
    )
    img = AsyncImage(source=data['picture_url'], allow_stretch=True, keep_ratio=False,
                     pos_hint={'center_x': .5, 'center_y': .5})

    superhost_chip = MDChip(
        text='SUPERHOST',
        pos_hint={'center_x': .24, 'center_y': .83},
        icon='',
        color=[1, 1, 1, 1],

    )
    staricon = MDIcon(
        icon='star',
        pos_hint={'center_x': .53, 'center_y': .76}
    )
    starlabel = MDLabel(
        text=f"[b]{float(data['review_score'])/20}[/b] ({data['number_of_reviews']})", markup=True,
        pos_hint={'center_x': .63, 'center_y': .75}
    )

    label = MDLabel(text=f"{data['room_type']}"
                         f"\n[b]{data['price']}$[/b]/night",
                    markup=True,
                    halign='left',
                    width=250,
                    size_hint=(None, None),
                    pos_hint={'center_x': .5, 'center_y': .5})

    bookmarkbutton = ListingSaveButton(data)

    webbutton = MDIconButton(
        icon='search-web',
        on_press=lambda x: open_link(data['listing_url']),
        user_font_size="36sp",
        pos_hint={'center_x': .90, 'center_y': .15}
    )

    imagebox.add_widget(img)
    textbox.add_widget(label)
    imagebox.add_widget(bookmarkbutton)
    textbox.add_widget(webbutton)
    textbox.add_widget(staricon)
    textbox.add_widget(starlabel)
    if data['is_superhost']:
        imagebox.add_widget(superhost_chip)
    superbox.add_widget(imagebox)
    superbox.add_widget(textbox)

    popup = Popup(
        content=superbox,
        background='background.jpg',
        size_hint=(None, None),
        size=(300, 350),
        pos_hint={'left': 0.9},
        auto_dismiss=True,
        separator_color=[.9, .4, .2, 1],
        background_color=[0, 0, 0, 0],
        on_dismiss=parent.reset_marker
        )

    return popup
