from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from components.ListingSaveButton import ListingSaveButton
import os
import requests
import json
from restAPIConnection import RestAPIConnection
from kivy.app import App
import time

def listingDetail(listing_id):
    #get Data
    custom_filters = {'id.eq':str(listing_id)}
    print("listingDetail")
    start = time.time()
    app = App.get_running_app()
    detail_data = [None]
    other_data = [None]
    start=time.time()
    app.api.getListingDetail(detail_data,custom_filters)
    start=time.time()
    app.api.getListingOther(other_data,custom_filters)

    #merge data
    data = {**detail_data[0][0], **other_data[0][0]}
    box = BoxLayout()
    img = AsyncImage(source=data['picture_url'])
    label = Label(text = f"Price: {data['price']}$/night\nRoomType: {data['room_type']}")
    print(ListingSaveButton)
    button = ListingSaveButton(data,text="Bookmark listing")

    print(data['picture_url'])
    box.add_widget(img)
    box.add_widget(label)
    box.add_widget(button)
    
    
    popup = Popup(
        title=data['name'],
        content=box,
        size_hint=(None,None),
        size=(600,600),
        auto_dismiss=True)
    
    return popup
    
