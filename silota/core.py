from .api import API

def from_key(api_key):
    h = API()
    h.authenticate(api_key)

    return h
