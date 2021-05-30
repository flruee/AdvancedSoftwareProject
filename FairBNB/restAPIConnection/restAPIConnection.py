import requests
import json


class RestAPIConnection:
    """
    Every API call gets through this class first. 
    It will store and apply filters.
    """
    def __init__(self, filters=None, base_url="http://localhost:8888"):
        self.base_url = base_url
        self.filters = {}
        self.filters = self.override_filter(filters)

    def set_filters(self, custom_filters):
        self.filters = self.override_filter(custom_filters)
        
        print(f"Current Filters:\n{self.filters}")

    def override_filter(self, custom_filters=None):
        filters = self.filters.copy()
        if custom_filters:
            for key in custom_filters.keys():

                filters[key] = custom_filters[key]
        filters = {k: v for k, v in filters.items() if v is not None}
    
        return filters

    def _GET(self, res, url, custom_filters, append):
        if append:
            filters = self.override_filter(custom_filters)
        else:
            filters = custom_filters
        for key in filters:
            if ".in" in key and filters[key] == []:
                filters[key] = ['']
        print(filters)
        resp = requests.get(url, params=filters)
        res[0] = json.loads(resp.text)

    def get_listing_location(self, res, custom_filters=None, append=True):
        url = self.base_url+"/listing_location"
        self._GET(res, url, custom_filters, append)
    
    def get_listing_detail(self, res, custom_filters=None, append=True):
        url = self.base_url+'/listing_detail'
        return self._GET(res, url, custom_filters, append)
    
    def get_listing_other(self, res, custom_filters=None, append=True):
        url = self.base_url+'/listing_other'
        return self._GET(res, url, custom_filters, append)
    
    def get_village_category(self, res, custom_filters=None, append=True):
        url = self.base_url+'/village_category'
        return self._GET(res, url, custom_filters, append)

    def get_reviews(self, res, custom_filters=None, append=True):
        url = self.base_url+'/reviews'
        return self._GET(res, url, custom_filters, append)
