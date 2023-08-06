import io
import unittest
from multiprocessing import Process

import requests
from drb.exceptions import DrbException
from requests.auth import HTTPBasicAuth

from drb_impl_http import DrbHttpNode
from tests.utility import start_auth_serve, PORT, PATH

process = Process(target=start_auth_serve)


class TestDrbHttpBasicAuth(unittest.TestCase):
    url_ok = 'http://localhost:' + PORT + PATH + 'test.txt'

    @classmethod
    def setUpClass(cls) -> None:
        process.start()

    @classmethod
    def tearDownClass(cls) -> None:
        process.kill()

    def test_attributes(self):
        key = 'Content-type'
        self.assertEqual(
            requests.head(self.url_ok).headers[key],
            DrbHttpNode(self.url_ok).get_attribute(key))

    def test_no_credential(self):
        node = DrbHttpNode(self.url_ok)
        with self.assertRaises(DrbException):
            node.get_impl(io.BytesIO).getvalue().decode()

    def test_wrong_credential(self):
        node = DrbHttpNode(self.url_ok, auth=HTTPBasicAuth("Bruce", "Wayne"))
        with self.assertRaises(DrbException):
            node.get_impl(io.BytesIO).getvalue().decode()

    def test_credential(self):
        node = DrbHttpNode(self.url_ok,
                           auth=HTTPBasicAuth('user', 'pwd123456'))
        self.assertEqual('{"path": "/tests/resources/test.txt"}',
                         node.get_impl(io.BytesIO).getvalue().decode())
