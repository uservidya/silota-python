

class Config(object):
    def __init__(self):
        super(Config, self).__init__()
        
        self.root_uri = 'https://api.silota.com'
        self.search_root_uri = 'https://search-sandbox.silota.com'
        self.version = 'v1'

    @property
    def uri(self):
        return '%s/%s' % (self.root_uri, self.version)


    @property
    def search_uri(self):
        return '%s/%s' % (self.search_root_uri, self.version)
