

class Config(object):
    def __init__(self):
        super(Config, self).__init__()
        
        self.root_uri = 'https://api.silota.com'
        self.version = 'v1'

    @property
    def uri(self):
        return '%s/%s' % (self.root_uri, self.version)
