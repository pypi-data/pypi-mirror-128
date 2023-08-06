import unittest

from drb import DrbNode
from drb_impl_http import DrbHttpNode, DrbHttpFactory
from tests.utility import PORT, PATH


class TestDrbHttpFactory(unittest.TestCase):

    def test_create(self):
        factory = DrbHttpFactory()
        node = factory.create('http://localhost:'+PORT+PATH+'test.txt')
        self.assertIsInstance(node, (DrbHttpNode, DrbNode))
