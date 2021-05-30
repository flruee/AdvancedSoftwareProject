from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.card import MDCard
from kivymd.uix.picker import MDDatePicker
from kivy.app import App
from kivymd.app import MDApp


class Form(MDCard):
    """
    Questionnaire Screen: here all the widgets seen on the questionnaire are initialised. Once an option is modified, it
    directly sets the filter for the REST-API get request. The search button is simply to switch the screen to the map.
    """
    def __init__(self, **kwargs):
        super(Form, self).__init__(**kwargs)
        self.interests = set()

    def on_start(self):
        """
        binds list items to widgets. The function is called once the Form class is initialised.
        """
        neighborhoods = [
            {"viewclass": "OneLineListItem",
             "text": "---",
             "on_release": lambda x=f"---": self.set_neighborhood(x),
             },
            {"viewclass": "OneLineListItem",
             "text": "Bronx",
             "on_release": lambda x=f"Bronx": self.set_neighborhood(x),
             },
            {"viewclass": "OneLineListItem",
             "text": "Brooklyn",
             "on_release": lambda x=f"Brooklyn": self.set_neighborhood(x),
             },
            {"viewclass": "OneLineListItem",
             "text": "Manhattan",
             "on_release": lambda x=f"Manhattan": self.set_neighborhood(x),
             },
            {"viewclass": "OneLineListItem",
             "text": "Queens",
             "on_release": lambda x=f"Queens": self.set_neighborhood(x),
             },
            {"viewclass": "OneLineListItem",
             "text": "Staten Island",
             "on_release": lambda x=f"Staten Island": self.set_neighborhood(x)
             }
        ]

        ages = [
            {"viewclass": "OneLineListItem",
             "text": "---",
             "on_release": lambda x=f"---": self.set_age(x),
             },
            {"viewclass": "OneLineListItem",
             "text": "18 - 30",
             "on_release": lambda x=f"18-30": self.set_age(x),
             },
            {"viewclass": "OneLineListItem",
             "text": "31 - 50",
             "on_release": lambda x=f"31-50": self.set_age(x),
             },
            {"viewclass": "OneLineListItem",
             "text": "50+",
             "on_release": lambda x=f"50+": self.set_age(x),
             }
        ]

        self.menu_n = MDDropdownMenu(
            caller=self.ids.field_n,
            items=neighborhoods,
            position="auto",
            width_mult=3,)
        self.menu_a = MDDropdownMenu(
            caller=self.ids.field_a,
            items=ages,
            position="auto",
            width_mult=2,)

        self.ids.field_g.bind(
            on_text_validate=self.set_error_message,
            on_focus=self.set_error_message)

        app = App.get_running_app()
        self.api = app.api

    def set_neighborhood(self, text__neighbor):
        """
        sets the borough filter

        Parameters
        ----------
        text__neighbor : str
        """
        if text__neighbor=='---':
            self.ids.field_n.text = text__neighbor
            borough_filter = {"borough.eq":None}
        else:
            self.ids.field_n.text = text__neighbor
            borough_filter = {"borough.eq":"'"+text__neighbor+"'"}
        self.menu_n.dismiss()
        self.api.set_filters(borough_filter)

    def set_guest(self, n_guests):
        """
        sets the guests_included filter

        Parameters
        ----------
        n_guests : int
        """
        guest_filter = {"guests_included.ge":n_guests}
        self.api.set_filters(guest_filter)


    def set_error_message(self, instance_textfield):
        """
        checks if the text of a textfield is numerical. If yes the content of the
        textfield will be relayed to set_guest, if not the textfield will display an
        error message.

        Parameters
        ----------
        instance_textfield : widget
        """
        g_num = instance_textfield.text
        if g_num.isdigit():
            g_num = int(g_num)
            if g_num not in list(range(1, 17)):
                self.ids.field_g.error = True
                return
            self.set_guest(g_num)
            self.ids.field_g.error = False
        else:
            self.ids.field_g.error = True
        

    def set_age(self, text__age):
        """
        sets the age filter

        Parameters
        ----------
        text__age : str
        """
        if text__age=="---":
            self.ids.field_a.text = ""
            age_filter = {"age.eq":None}
        else:
            self.ids.field_a.text = text__age
            age_filter = {"age.eq": f"'{text__age}'"}
        self.api.set_filters(age_filter)
        self.menu_a.dismiss()
        res = [None]
        self.api.get_village_category(res, age_filter)
        village_list = []
        for i in res[0]:
            village_list.append(i[0])
            
        village_filter = {"village.in[]":village_list}
        self.api.set_filters(village_filter)


    def set_interest(self, instance_chips):
        """
        adds/removes interests to a set and updated interest filters

        Parameters
        ----------
        instance_chips : widget
        """
        if instance_chips.color == [0, 0, 0, 0.1]:
            instance_chips.color = [252/255, 186/255, 3/255, 1]
            self.interests.add(instance_chips.text)
        else:
            instance_chips.color = [0, 0, 0, 0.1]
            self.interests.discard(instance_chips.text)
        interest_filter = {"interest.in[]":self.interests}
        self.api.set_filters(interest_filter)
        res = [None]    
        self.api.get_village_category(res,interest_filter)
        village_list = []
        for i in res[0]:
            village_list.append(i[0])
        village_filter = {"village.in[]": village_list}
        self.api.set_filters(village_filter)



    def set_highrating(self, status):
        """
        sets the highrating filter

        Parameters
        ----------
        status : bool
        """
        rating_filter = {"review_score.ge":None}
        if(status):
            rating_filter["review_score.ge"] = 90
        self.api.set_filters(rating_filter)

    def set_superhost(self, status):
        """
        sets the superhost filter

        Parameters
        ----------
        status : bool
        """
        superhost_filter = {"is_superhost.eq": None}
        if status:
            superhost_filter['is_superhost.eq'] = True
        self.api.set_filters(superhost_filter)

    def set_fairfilter(self, status):
        """
        sets the fairfilter filter

        Parameters
        ----------
        status : bool
        """
        fair_filter = {"total_listings_count.le": None}
        if status:
            fair_filter['total_listings_count.le'] = 3
        self.api.set_filters(fair_filter)

    def set_price(self):
        """
        sets the price on the range slider. 
        """
        min_p, max_p = self.ids.min_p.text, self.ids.max_p.text
        if min_p=="" or not min_p.isdigit():
            min_p=self.ids.price_filter.min
        if max_p=="" or not max_p.isdigit():
            max_p=self.ids.price_filter.max

        self.ids.price_filter.value1 = int(min_p)
        self.ids.price_filter.value2=int(max_p)

    def switch_to_mapscreen(self):
        """
        sets the price filter and switches to mapscreen
        """
        price_range=self.ids.price_filter.value
        if(price_range[0]==0):
            price_range[0]=None
        if(price_range[1]==9999):
            price_range[1]=None
        price_filter = {"price.ge":price_range[0],"price.le":price_range[1]}
        
        self.api.set_filters(price_filter)
        app = App.get_running_app()

        screenmanager = app.root.ids['screen_manager']
        screenmanager.current = "mapscreen"
        mapview = app.root.ids['mapview']


if __name__ == "__main__":

    class SliderApp(MDApp):
        def build(self):
            return Form()


    SliderApp().run()
