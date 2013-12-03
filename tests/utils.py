import contextlib
import multiprocessing
import unittest2 as unittest
from wsgiref.simple_server import make_server

SILOTA_TEST_SERVER_PORT = 62187
SILOTA_TEST_SEARCH_SERVER_PORT = 62188

class WSGIServerTest(unittest.TestCase):

    def setUp(self):
        self.server_process = None

    @contextlib.contextmanager
    def start_server(self, app, port=SILOTA_TEST_SERVER_PORT):
        server = make_server('', port, app)
        self.server_process = multiprocessing.Process(
            target=server.serve_forever
        )
        try:
            self.server_process.start()
            yield
        finally:
            self._stop_server()

    def _stop_server(self):
        self.server_process.terminate()
        self.server_process.join()
        del self.server_process
        self.server_process = None


    @contextlib.contextmanager
    def start_search_server(self, app, port=SILOTA_TEST_SEARCH_SERVER_PORT):
        server = make_server('', port, app)
        self.search_server_process = multiprocessing.Process(
            target=server.serve_forever
        )
        try:
            self.search_server_process.start()
            yield
        finally:
            self._stop_search_server()

    def _stop_search_server(self):
        self.search_server_process.terminate()
        self.search_server_process.join()
        del self.search_server_process
        self.search_server_process = None
