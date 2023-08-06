import io
import unittest
from multiprocessing import Process

import requests
from drb.exceptions import DrbException

from drb_impl_http import DrbHttpNode
from tests.utility import start_serve, PATH
from tests.utility import PORT

process = Process(target=start_serve)


class TestDrbHttp(unittest.TestCase):
    url_ok = 'http://localhost:' + PORT + PATH + 'test.txt'
    url_false = 'http://localhost:' + PORT + PATH + 'test.json'

    @classmethod
    def setUpClass(cls) -> None:
        process.start()

    @classmethod
    def tearDownClass(cls) -> None:
        process.kill()

    def test_impl_download(self):
        node = DrbHttpNode(self.url_ok)
        self.assertEqual('This is my awesome test.',
                         node.get_impl(io.BytesIO).getvalue().decode())

    def test_impl_argument(self):
        key = ('params', None)
        self.assertEqual(
            requests.head(self.url_ok,
                          params={'key': 'value'}).headers[key[0]],
            DrbHttpNode(self.url_ok,
                        params={'key': 'value'}).attributes[key]
        )

    def test_impl_none_argument(self):
        key = ('params', None)
        with self.assertRaises(KeyError):
            DrbHttpNode(self.url_ok, params=None).attributes[key]

    def test_impl_no_argument(self):
        key = ('params', None)
        with self.assertRaises(KeyError):
            DrbHttpNode(self.url_ok).attributes[key]

    def test_check_class(self):
        self.assertTrue(issubclass(DrbHttpNode, DrbHttpNode))

    def test_name(self):
        node = DrbHttpNode(self.url_ok)
        self.assertEqual('test.txt', node.name)

    def test_namespace_uri(self):
        node = DrbHttpNode(self.url_ok)
        self.assertIsNone(node.namespace_uri)

    def test_value(self):
        path = self.url_ok
        self.assertIsNone(DrbHttpNode(path).value)

    def test_parent(self):
        node = DrbHttpNode(self.url_ok)
        self.assertIsNone(node.parent)

    def test_attributes(self):
        key = ('Content-type', None)
        self.assertEqual(
            requests.head(self.url_ok).headers[key[0]],
            DrbHttpNode(self.url_ok).attributes[key])

    def test_wrong_attributes(self):
        with self.assertRaises(DrbException):
            DrbHttpNode(self.url_ok).get_attribute('A Wrong attributes', None)
        with self.assertRaises(DrbException):
            DrbHttpNode(self.url_ok).get_attribute('A Wrong attributes',
                                                   'Something')
        with self.assertRaises(DrbException):
            DrbHttpNode(self.url_ok).get_attribute('Content-Type',
                                                   'Something')

    def test_path(self):
        self.assertEqual(self.url_ok, DrbHttpNode(self.url_ok).path.name)

    def test_children(self):
        self.assertEqual(0, len(DrbHttpNode(self.url_ok).children))

    def test_hash_children(self):
        self.assertFalse(DrbHttpNode(self.url_ok).has_child)

    def test_get_attribute(self):
        node = DrbHttpNode(self.url_ok)
        self.assertEqual(
            'text/plain',
            node.get_attribute('Content-type'))
        node2 = DrbHttpNode(self.url_false)

        with self.assertRaises(DrbException):
            node2.get_attribute('Connection')

        with self.assertRaises(DrbException):
            node.get_attribute('foobar')

    def test_has_child(self):
        self.assertFalse(DrbHttpNode(self.url_ok).has_child)
