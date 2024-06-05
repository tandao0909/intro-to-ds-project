from geopy.geocoders import Nominatim
import time
import numpy as np
import requests

app = Nominatim(user_agent="yusnivtr")
def get_location_by_address(address):
    time.sleep(1)
    if address == "na":
        return None
    try:
        location =  app.geocode(address).raw
        latitude = location["lat"]
        longitude = location["lon"]
        return(latitude,longitude)
    except:
        # return get_location_by_address(address)
        return np.nan