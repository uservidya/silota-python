import bottle
import json
from .responses import get_engines, get_topics, get_schema, get_templates

SERIALIZERS = {
    'application/json': json.dumps,
    }

SILOTA_TEST_API_KEY = 'THISISAKEY'

app = bottle.Bottle()
search_app = bottle.Bottle()


@search_app.get('/jsc/<engine_id>.js')
def payload_build(engine_id):
    bottle.response.body = ''
    return bottle.response

@app.hook('before_request')
def auth():
    key = bottle.request.headers.get('Authorization', None)
    if key:
        token = key.split()
        if len(token) == 2 and token[0].lower() == 'basic':
            if token[1] == SILOTA_TEST_API_KEY:
                return True

    raise bottle.HTTPError(status=401)

@app.get('/engines/')
def engines():
    bottle.response.content_type = (
        bottle.request.headers.get('Accept', 'application/json'))
    serializer = SERIALIZERS[bottle.response.content_type]

    the_response = get_engines()

    bottle.response.body = serializer(the_response)
    return bottle.response
    
@app.get('/engine/<engine_id>/topics/')
def topics(engine_id):
    bottle.response.content_type = (
        bottle.request.headers.get('Accept', 'application/json'))
    serializer = SERIALIZERS[bottle.response.content_type]

    the_response = get_topics(engine_id=int(engine_id))

    bottle.response.body = serializer(the_response)
    return bottle.response


@app.get('/topic/<topic_id>/schema/')
def schema(topic_id):
    bottle.response.content_type = (
        bottle.request.headers.get('Accept', 'application/json'))
    serializer = SERIALIZERS[bottle.response.content_type]

    the_response = get_schema(topic_id = int(topic_id))
    
    bottle.response.body = serializer(the_response)
    return bottle.response

@app.get('/topic/<topic_id>/templates/')
def templates(topic_id):
    bottle.response.content_type = (
        bottle.request.headers.get('Accept', 'application/json'))
    serializer = SERIALIZERS[bottle.response.content_type]

    the_response = get_templates(topic_id = int(topic_id))
    
    bottle.response.body = serializer(the_response)
    return bottle.response


app.mount('/v1', app)
search_app.mount('/v1', search_app)
