from kivy.uix.button import Button
from kivy.app import App


class ResetFilterButton(Button):
    """
    Creates a "Reset Filters" Button iff some filters are already set (to be precise after the "Apply filters" button was pressed).
    On click it will reset all filters in the RestAPIConnection class.
    """
    def __init__(self, *args, **kwargs):
        super(ResetFilterButton, self).__init__(*args, **kwargs)
        self.text = 'Reset Filters'
        self.hide()

    def on_release(self):
        # resets current Filters on api
        app = App.get_running_app()
        filter_menu = app.root.ids.filter_menu

        price_filter = filter_menu.ids.price_filter
        price_filter._set_value((price_filter.min,price_filter.max))    

        age_filter = filter_menu.ids.age_filter
        age_filter._set_value((age_filter.min,age_filter.max))

        filters = {
            "price.ge": None,
            "price.le": None,
            "age.ge": None,
            "age.le": None
        }
        app.api.set_filters(filters)
        self.hide()

    def show(self):
        self.disabled = False
        self.opacity = 1
    
    def hide(self):
        self.disabled = True
        self.opacity = 0


class ApplyFilterButton(Button):
    """
    Creates an "Apply Filter" button.
    On click it will set the filters on the RestAPIConnection class.
    """
    def __init__(self, *args, **kwargs):
        super(ApplyFilterButton, self).__init__(*args, **kwargs)
        self.text = 'Apply filters'

    def on_release(self):
        # Sets apiConnection filters according to filters
        # TODO add feedback
        app = App.get_running_app()
        filter_menu = app.root.ids.filter_menu
        price_filter = filter_menu.ids.price_filter

        age_filter = filter_menu.ids.age_filter

        filter = {
            "price.ge":int(price_filter.value[0]),
            "price.le":int(price_filter.value[1]),
            "age.ge":int(age_filter.value[0]),
            "age.le":int(age_filter.value[1])
        }
        app.api.set_filters(filter)
        resetFilter = filter_menu.ids.reset_filters
        resetFilter.show()
