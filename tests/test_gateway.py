from starlette.responses import HTMLResponse
from starlette.testclient import TestClient

import unittest

from gateway import app


class TestApi(unittest.TestCase):

    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_register(self):
        response = self.client.post('/reg')
        print(response.content)
        print(response.headers)
        print(response.status_code)
