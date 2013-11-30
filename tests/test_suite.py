from requests.exceptions import HTTPError

from .utils import WSGIServerTest, SILOTA_TEST_SERVER_PORT
from .application import app, SILOTA_TEST_API_KEY

import silota


class Suite(WSGIServerTest):
    def setUp(self):
        super(Suite, self).setUp()
        silota.config.root_uri = 'http://localhost:%d' % SILOTA_TEST_SERVER_PORT

    def test_01_wrong_auth(self):
        with self.start_server(app):
            client = silota.from_key('foo')
            with self.assertRaises(HTTPError):
                engines = client.engines

    def test_02_right_auth(self):
        with self.start_server(app):
            client = silota.from_key(SILOTA_TEST_API_KEY)
            engines = client.engines
            self.assertEquals(len(engines), 2)
            

    def test_03_get_engine(self):
        with self.start_server(app):
            client = silota.from_key(SILOTA_TEST_API_KEY)
            engines = client.engines
            for eng in engines:
                eng2 = client.engines[eng.id]
                self.assertEqual(eng2.name, eng.name)

    def test_04_get_wrong_engine(self):
        with self.start_server(app):
            client = silota.from_key(SILOTA_TEST_API_KEY)
            with self.assertRaises(KeyError):
                engine = client.engines[74983342]

    def test_05_create_engine(self):
        pass


    def test_06_get_topics(self):
        with self.start_server(app):
            client = silota.from_key(SILOTA_TEST_API_KEY)
            engines = client.engines
            for eng in engines:
                topics = eng.topics
                if eng.id == 1403592042880088015:
                    self.assertEqual(len(topics), 1)
                else:
                    self.assertEqual(len(topics), 0)
                

    def test_07_get_wrong_topic(self):
        with self.start_server(app):
            client = silota.from_key(SILOTA_TEST_API_KEY)
            engine = client.engines[1403592042880088015]
            with self.assertRaises(KeyError):
                topic = engine.topics[2332322]
                

    def test_08_create_topics(self):
        pass

    def test_09_get_schema(self):
        pass

    def test_10_set_schema(self):
        pass

    def test_11_set_schema_wrong_format(self):
        pass

    def test_12_get_templates(self):
        pass

    def test_13_set_templates(self):
        pass

    def test_14_set_templates_garbage(self):
        pass

    def test_15_get_documents(self):
        pass

    def test_16_get_documents_pagination(self):
        pass

    def test_17_index_document_with_id(self):
        pass

    def test_18_index_document_without_id(self):
        pass

    def test_19_bulk_index(self):
        pass

    def test_20_bulk_update(self):
        pass




