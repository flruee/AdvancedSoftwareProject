from kivymd.uix.card import MDCard
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.slider import Slider
from kivy.uix.button import Button

from .rangeSlider import RangeSlider
from .filterButtons import ApplyFilterButton, ResetFilterButton

kv = '''
<FilterMenu>:
    BoxLayout:
        orientation: 'vertical'
        MDLabel:
            text: 'Price'
            opposite_colors:True


        RangeSlider:
            id: price_filter
            value: 0,9999
            min:0
            max:9999

        BoxLayout:
            MDLabel:
                text: 'Minimum Price: {}'.format(int(price_filter.value[0]))
                color: 0.5,0.5,0.5,1
            MDLabel:
                text: 'Maximum Price {}'.format(int(price_filter.value[1]))


        MDLabel:
            text: 'Age'
            color: 0,0,0,1
        RangeSlider:
            id: age_filter
            value: 0,99
        BoxLayout:
            MDLabel:
                text: 'Minimum Age: {}'.format(int(age_filter.value[0]))
            MDLabel:
                text: 'Maximum Age: {}'.format(int(age_filter.value[1]))


        ApplyFilterButton
        ResetFilterButton:
            id: reset_filters
'''


class FilterMenu(MDCard):
    def __init__(self, *args, **kwargs):
        super(FilterMenu, self).__init__(*args, **kwargs)

    def build(self):
        return Builder.load_string(kv)


if __name__ == "__main__":
    from kivy.app import App

    """
    Builder.load_string('''
<FilterMenu>:

    orientation: 'vertical'
    BoxLayout:
        orientation: 'vertical'
        MDLabel:
            text: 'Price'

        RangeSlider:
            id: price_filter
            value: 0,9999
            min:0
            max:9999

        BoxLayout:
            MDLabel:
                text: 'Minimum Price: {}'.format(int(price_filter.value[0]))
            MDLabel:
                text: 'Maximum Price {}'.format(int(price_filter.value[1]))


        MDLabel:
            text: 'Age'
        RangeSlider:
            id: age_filter
            value: 0,99
        BoxLayout:
            MDLabel:
                text: 'Minimum Age: {}'.format(int(age_filter.value[0]))
            MDLabel:
                text: 'Maximum Age: {}'.format(int(age_filter.value[1]))


        ApplyFilterButton
        ResetFilterButton:
            id: reset_filters
    ''')
    """


    class FilterMenuApp(BoxLayout):
        pass


    class SliderApp(MDApp):
        def build(self):
            return FilterMenu()


    SliderApp().run()