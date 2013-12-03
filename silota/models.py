try:
    from simplejson import loads as json_decode, dumps as json_encode
except ImportError:
    from json import loads as json_decode, dumps as json_encode

import urllib

from .helpers import to_python
from .structures import PagedKeyedListResource

class BaseResource(object):
    _strs = []
    _ints = []
    _dates = []
    _bools = []
    _dicts = []
    _map = {}
    _pks = []

    def __init__(self):
        self._bootstrap()
        self._h = None
        super(BaseResource, self).__init__()

    def __repr__(self):
        return "<resource '{0}'>".format(self._id)

    def _bootstrap(self):
        """Bootstraps the model object based on configured values."""

        for attr in self._keys():
            setattr(self, attr, None)

    def _keys(self):
        return self._strs + self._ints + self._dates + self._bools + self._map.keys()

    @property
    def _id(self):
        try:
            return getattr(self, self._pks[0])
        except IndexError:
            return None

    @property
    def _ids(self):
        """The list of primary keys to validate against."""
        for pk in self._pks:
            yield getattr(self, pk)

        for pk in self._pks:

            try:
                yield str(getattr(self, pk))
            except ValueError:
                pass

    def dict(self):
        d = dict()
        for k in self.keys():
            d[k] = self.__dict__.get(k)

        return d

    @classmethod
    def new_from_dict(cls, d, h=None, **kwargs):

        d = to_python(
            obj=cls(),
            in_dict=d,
            str_keys=cls._strs,
            int_keys=cls._ints,
            date_keys=cls._dates,
            bool_keys=cls._bools,
            dict_keys= cls._dicts,
            object_map=cls._map,
            _h = h
        )

        d.__dict__.update(kwargs)

        return d


class Rule(BaseResource):
    _pks = ['id']
    _ints = ['id', ]
    _strs = ['match', 'arg']
    _bools = ['does']

    def __init__(self):
        super(Rule, self).__init__()

    def __repr__(self):
        return "<rule: {0} {1} '{2}'>".format('does' if self.does else 'does not', self.match, self.arg)

    def new(self, id, does, match, arg):
        '''Create a new Rule for this feed'''

        #import pdb; pdb.set_trace()
        # brand new rule
        rules = [{'does': r.does,
                  'match': r.match,
                  'arg': r.arg,
                  'id': r.id} \
                 for r in self.feed.rules]
        existing_ids = [r.id for r in self.feed.rules]
        if id == None:
            rules.append({'does': does,
                          'match': match,
                          'arg': arg})

            payload = {'rules': rules}
            r = self._h._http_resource(
                method = 'PUT',
                resource = ('feed', self.feed.id, 'rules'),
                data = payload
                )

            # what's the new rule.
            for r in json_decode(r.content)['results']:
                if r['id'] not in existing_ids:
                    return self.feed.rules.get(r['id'])
        else:
            for r in rules:
                if r['id'] == id:
                    r['does'] = does
                    r['match'] = match
                    r['arg'] = arg
                    break
            payload = {'rules': rules}
            r = self._h._http_resource(
                method = 'PUT',
                resource = ('feed', self.feed.id, 'rules'),
                data = payload
                )
            for r in json_decode(r.content)['results']:
                if r['id'] == id:
                    return self.feed.rules.get(r['id'])
                


    def _new(self, has, match, arg):
        '''Create a new Rule'''

        rules = [{'has': r.has,
                  'match': r.match,
                  'arg': r.arg,
                  'id': r.id} \
                 for r in self.feed.rules]
        existing_ids = [r.id for r in self.feed.rules]
        rules.append({'has': has,
                      'match': match,
                      'arg': arg})

        payload = {'rules': rules}

        r = self._h._http_resource(
            method = 'PUT',
            resource = ('feed', self.feed.id, 'rules'),
            data = payload
            )

        # what's the new rule.
        for r in json_decode(r.content)['results']:
            if r['id'] not in existing_ids:
                return self.feed.rules.get(r['id'])
        

class Feed(BaseResource):
    _pks = ['id', ]
    _ints = ['id', ]
    _strs = ['type', 'name', 'url', 'sitemap_url']
    _dicts = ['options']
    _dates = ['updated_at', 'last_run']

    def __init__(self):
        super(Feed, self).__init__()

    def __repr__(self):
        return "<feed '{0}'>".format(self.name)

    def new(self, url, sitemap_url, name=None):
        '''Create a new feed'''

        payload = {}
        payload['url'] = url
        payload['sitemap_url'] = sitemap_url
        payload['name'] = name

        r = self._h._http_resource(
            method = 'POST',
            resource = ('topic', self.topic.id, 'feeds'),
            data = payload
            )
        id = json_decode(r.content).get('id')
        return self.topic.feeds.get(id)

    def delete(self):
        r = self._h._http_resource(
            method='DELETE',
            resource=('feed', self.id)
        )
        return r.ok

    @property
    def rules(self):
        return self._h._get_resources(
            resource=('feed', self.id, 'rules'),
            obj=Rule, feed=self)


class Source(BaseResource):
    _pks = ['id', ]
    _ints = ['id', ]
    _strs = ['label', 'url' ]
    _dicts = ['conditions']

    def __init__(self):
        super(Source, self).__init__()
    
    def __repr__(self):
        return "<source '{0}'>".format(self.label)

    def new(self, url, label, type, selector_dict):
        '''Create a new topic'''

        payload = {}
        payload['url'] = url
        payload['label'] = label
        payload['type'] = type
        payload['selector_dict'] = selector_dict

        r = self._h._http_resource(
            method = 'POST',
            resource = ('topic', self.topic.id, 'sources'),
            data = payload
            )
        id = json_decode(r.content).get('id')
        return self.topic.sources.get(id)

class Document(BaseResource):
    _pks = ['id', ]
    _strs = ['id', 'url', ] 
    _dates = ['updated_at', ]
    
    def __init__(self):
        super(Document, self).__init__()
    
    def __repr__(self):
        return "<document '{0}'>".format(self.id)

    def new(self, **kwargs):
        '''Create/Index a new document'''

        payload = {}
        payload.update(kwargs)

        r = self._h._http_resource(
            method = 'POST',
            resource = ('topic', self.topic.id, 'documents'),
            data = payload
            )

        #id = json_decode(r.content).get('id')
        #return self.topic.documents.get(id)
        return json_decode(r.content)

    @classmethod
    def new_from_dict(cls, d, h=None, **kwargs):
        # Override normal operation because of crazy api.
        obj = to_python(
            obj=cls(),
            in_dict=d,
            str_keys=cls._strs,
            int_keys=cls._ints,
            date_keys=cls._dates,
            bool_keys=cls._bools,
            dict_keys= cls._dicts,
            object_map=cls._map,
            _h = h
        )

        c = cls()
        #c.data = d
        c._h = h
        #c.topic = kwargs.get('topic')

        for k, v in d.iteritems():
            if k in obj.__dict__:
                c.__setattr__(k, obj.__dict__[k])
            else:
                c.__setattr__(k, v)

        return c

    def delete(self):
        r = self._h._http_resource(
            method='DELETE',
            resource=('document', self.id)
        )
        return r.ok

class Templates(BaseResource):
    _strs = ['serp', 'suggest']

    def __init__(self):
        super(Templates, self).__init__()

    def __repr__(self):
        return "<templates '{0}'>".format('lala')

    def update(self, serp=None, suggest=None):
        payload = {}
        if serp:
            payload['serp'] = serp
        if suggest:
            payload['suggest'] = suggest
        r = self._h._http_resource(
            method = 'PUT',
            resource = ('topic', self.topic.id, 'templates'),
            data = payload
        )


class Schema(object):
    def __init__(self):
        self.data = []
        self.topic = None
        self._h = None

        super(Schema, self).__init__()

    def __repr__(self):
        return repr(self.data)

    @classmethod
    def new_from_dict(cls, d, h=None, **kwargs):
        # Override normal operation because of crazy api.
        c = cls()
        c.data = d
        c._h = h
        c.topic = kwargs.get('topic')

        return c

    def update(self, schema):
        payload = schema
        r = self._h._http_resource(
            method='PUT',
            resource=('topic', self.topic.id, 'schema'),
            data = payload
            )
        return r.content
    
    def __iter__(self):
        for item in self.data:
            yield item


class Topic(BaseResource):
    _pks = ['id', ]
    _ints = ['id', ]
    _strs = ['name', 'suggest_template', 'serp_template' ]
    _bools = ['draft', ]
    _dates = ['updated_at', 'last_crawl']

    def __init__(self):
        super(Topic, self).__init__()
    
    def __repr__(self):
        return "<topic '{0}'>".format(self.name)

    def new(self, name=None):
        '''Create a new topic'''

        payload = {}
        payload['name'] = name

        r = self._h._http_resource(
            method = 'POST',
            resource = ('engine', self.engine.id, 'topics'),
            data = payload
            )

        id = json_decode(r.content).get('id')
        return self.engine.topics.get(id)


    def delete(self):
        r = self._h._http_resource(
            method='DELETE',
            resource=('topic', self.id)
        )
        return r.ok

    @property
    def feeds(self):
        return self._h._get_resources(
            resource=('topic', self.id, 'feeds'),
            obj=Feed, topic=self)

    def get_documents(self, page=1):
        return self._h._get_resources(
            resource=('topic', self.id, 'documents'),
            #obj=Document, map=PagedKeyedListResource, topic=self, params={'page': page})
            obj=Document, map=PagedKeyedListResource, topic=self, params={})

    documents = property(get_documents)

    def delete_documents(self):
        r = self._h._http_resource(
            method='DELETE',
            resource=('topic', self.id, 'delete_documents')
        )
        return r.ok

    @property
    def schema(self):
        return self._h._get_resource(
            resource=('topic', self.id, 'schema'),
            obj=Schema, topic=self)

    @property
    def templates(self):
        return self._h._get_resource(
            resource=('topic', self.id, 'templates'),
            obj=Templates, topic=self)

    def crawl(self, force=False):
        if not force:
            r = self._h._http_resource(
                method='POST',
                resource=('topic', self.id, 'crawl'))
        else:
            r = self._h._http_resource(
                method='POST',
                resource=('topic', self.id, 'crawl', 'force'))
        return r.json()

    def suggest(self, q):
        r = self._h._http_resource(
            method='GET',
            resource=('topic', self.id, 'suggest'),
            params={'q': q,
                    })
        return r.json()

class Engine(BaseResource):
    _pks = ['id', ]
    _ints = ['id', ]
    _strs = ['name', 'selectors']

    def __init__(self):
        super(Engine, self).__init__()

    def __repr__(self):
        return "<engine '{0}'>".format(self.name)
    
    def new(self, name=None):
        '''Create a new engine'''

        payload = {}
        payload['name'] = name

        r = self._h._http_resource(
            method = 'POST',
            resource = ('engines', ),
            data = payload
            )

        id = json_decode(r.content).get('id')
        return self._h.engines.get(id)

    def delete(self):
        r = self._h._http_resource(
            method='DELETE',
            resource=('engine', self.id)
        )
        return r.ok

    def update(self, name=None, selectors=None):
        if name == None:
            name = self.name
        else:
            self.name = name

        if selectors == None:
            selectors = self.selectors
        else:
            self.selectors = selectors

        payload = {'name': name, 'selectors': selectors}
        r = self._h._http_resource(
            method='PUT',
            resource=('engine', self.id),
            data = payload
        )
        id = json_decode(r.content).get('id')
        return self._h.engines.get(id)
        #return r.ok

        
    @property
    def topics(self):
        return self._h._get_resources(
            resource=('engine', self.id, 'topics'),
            obj=Topic, engine=self)

    def build_payload(self):
        # Just to avoid circular dependencies
        import silota as _s
        payload = {'topics': [], 'selectors': []}
        payload['selectors'] = [x for x in self.selectors]
        payload['selectors'].append('#console  .form-search  .search-box  .search-query')
        for topic in self.topics:
            d = {'id': topic.id, 'name': topic.name}
            d['fields'] = [x for x in topic.schema]
            d['templates'] = {}
            d['templates']['suggest'] = topic.templates.suggest
            payload['topics'].append(d)

        url_args = urllib.quote(json_encode(payload))
        url = '%s/jsc/%d.js?%s' % (_s.config.search_uri,
                                   self.id, url_args)
        r = self._h._session.get(url)

        r.raise_for_status()
        return r.content

