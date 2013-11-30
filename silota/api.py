try:
    from simplejson import loads as json_decode, dumps as json_encode
except ImportError:
    from json import loads as json_decode, dumps as json_encode

import requests
from requests.exceptions import HTTPError

from .helpers import is_collection
from .structures import KeyedListResource, PagedKeyedListResource
from .models import Engine

import silota

class APICore(object):
    def __init__(self, session=None):
        super(APICore, self).__init__()

        if session is None:
            session = requests.session()

        self._api_key = None
        self._api_key_verified = None
        self._session = session

        # We only want JSON back.
        self._session.headers.update({'Accept': 'application/json'})

        # We only send JSON
        self._session.headers.update({'content-type': 'application/json'})

        # Send version numbers
        self._session.headers.update({'User-agent': 'silota-python/' + silota.__version__})

    def __repr__(self):
        return '<api-core at 0x%x>' % (id(self))

    def authenticate(self, api_key):
        """Logs user into Heroku with given api_key."""
        self._api_key = api_key

        # Attach auth to session.
        self._session.headers['Authorization'] = 'Basic %s' % self._api_key
        return self._verify_api_key()

    def _verify_api_key(self):
        r = self._session.get(self._url_for('engines'))
        self._api_key_verified = True if r.ok else False
        return self._api_key_verified

    def _url_for(self, *args):
        args = map(str, args)
        return '/'.join([silota.config.uri] + list(args)) + '/'


    def _http_resource(self, method, resource, params=None, data=None):
        """Makes an HTTP request."""

        if not is_collection(resource):
            resource = [resource]

        # This is needed because we only send application/json
        data = json_encode(data)

        url = self._url_for(*resource)
        r = self._session.request(method, url, params=params, data=data)

        if r.status_code == 422:
            http_error = HTTPError('%s Client Error: %s' % (r.status_code, r.content))
            http_error.response = r
            raise http_error

        r.raise_for_status()
        return r


    @staticmethod
    def _resource_deserialize(s):
        """Returns dict deserialization of a given JSON string."""

        try:
            return json_decode(s)
        except ValueError:
            raise ResponseError('The API Response was not valid.')

    def _get_resource(self, resource, obj, params=None, **kwargs):
        """Returns a mapped object from an HTTP resource."""
        r = self._http_resource('GET', resource, params=params)
        item = self._resource_deserialize(r.content)

        return obj.new_from_dict(item, h=self, **kwargs)


    def _get_resources(self, resource, obj, params=None, map=None, **kwargs):
        r = self._http_resource('GET', resource, params=params)
        d_items = self._resource_deserialize(r.content)

        if type(d_items) == dict:
            items = [obj.new_from_dict(item, h=self, **kwargs) for item in d_items['results']]
        else:
            import pdb; pdb.set_trace()
            assert False

        if map is None:
            map = KeyedListResource

        list_resource = map(items=items)
        list_resource._h = self
        list_resource._obj = obj
        list_resource._kwargs = kwargs

        if map == PagedKeyedListResource:
            list_resource._count = d_items['pagination']['count']


        # if non default map, stuff the result of the response into the dict
        # if type(d_items) == dict:
        #     list_resource._count = d_items['count']
        #     list_resource._next = d_items['next']
        #     list_resource._previous = d_items['previous']

        return list_resource


class API(APICore):
    def __init__(self, session=None):
        super(API, self).__init__(session=session)

    def __repr__(self):
        return '<client at 0x%x>' % (id(self))

    @property
    def engines(self):
        return self._get_resources(('engines'), Engine)


class ResponseError(ValueError):
    """The API Response was unexpected."""

