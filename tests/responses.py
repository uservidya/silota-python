from json import dumps as json_encode


def _paginate(body):
    return {"pagination": len(body),
            "results": body}

_topics = [{
    "active": True, 
    "engine": 1403592042880088015,
    "id": 4848024419736434708, 
    "last_crawl": None, 
    "name": "First topic", 
    "order": 0,
    "serp_template": "",
    "suggest_template": "",
    "created_at": "2013-06-17T11:14:05.437Z", 
    "updated_at": "2013-06-17T11:14:05.585Z"
}]

_schema = {
    4848024419736434708: [{
        "name": "title",
        "type": "string",
        "search_enabled": True,
        "result_enabled": True,
    }, {
        "name": "content",
        "type": "text",
        "search_enabled": True,
        "result_enabled": True,
    }]
}

_templates = {
    4848024419736434708: {
        'serp': '',
        'suggest': ''
    }
}

def get_templates(topic_id):
    return _templates[topic_id]

def get_schema(topic_id):
    return _schema[topic_id]

def get_topics(engine_id, topic_id=None):
    topics = [x for x in _topics if x['engine'] == engine_id]
    if topic_id:
        return _paginate([x for x in topics if x['id'] == topic_id])
    return _paginate(topics)

def get_engines(id=None):
    _engines = [{
        "active": True, 
        "id": 1403592042880088015, 
        "name": "Engine 1",
        "selectors": [],
        "created_at": "2013-06-17T11:14:05.437Z", 
        "updated_at": "2013-06-17T11:14:05.585Z"
    }, {
        "active": True, 
        "id": 4866862347068170765, 
        "name": "Engine 2",
        "selectors": [],
        "created_at": "2013-06-17T11:14:05.437Z", 
        "updated_at": "2013-06-17T11:14:05.585Z"
    }]
    if id:
        return _paginate([x for x in _engines if x['id'] == id])
    return _paginate(_engines)
