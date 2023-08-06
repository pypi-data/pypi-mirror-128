import io
import unittest

from drb.exceptions import DrbException

from drb_impl_http import DrbHttpNode
from drb_impl_http.Bearer import Bearer
from tests.utility import stop_mock_oauth2_serve, start_mock_oauth2_serve


class TestDrbHttpOAuth2(unittest.TestCase):
    url_ok = 'https://something.com/resources/test.txt'
    url_ko = 'https://something.com/resources/not_here.txt'
    service_url = 'https://something.com/'
    token = '06b485119f019b90499bc08683be27cae85f2be5ad9a707989b79698a7f1bb22'

    @classmethod
    def setUpClass(cls) -> None:
        start_mock_oauth2_serve(cls.service_url)

    @classmethod
    def tearDownClass(cls) -> None:
        stop_mock_oauth2_serve()

    def test_Oauth2_wrong_user(self):
        node = DrbHttpNode(
            self.url_ok,
            Bearer('not_a_token')
        )
        with self.assertRaises(DrbException):
            node.get_impl(io.BytesIO).getvalue().decode()

    def test_Oauth2_download(self):

        node = DrbHttpNode(
            self.url_ok,
            Bearer(self.token)
        )
        self.assertEqual('This is my awesome test.',
                         node.get_impl(io.BytesIO).getvalue().decode())

    def test_Oauth2_not_here(self):
        node = DrbHttpNode(
            self.url_ko,
            Bearer(self.token)
        )
        with self.assertRaises(DrbException):
            node.get_impl(io.BytesIO).getvalue().decode()
