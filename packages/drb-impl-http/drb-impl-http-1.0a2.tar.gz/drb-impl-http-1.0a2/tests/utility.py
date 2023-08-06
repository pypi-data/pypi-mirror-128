import base64
import http
import json
import os
from http.server import HTTPServer, CGIHTTPRequestHandler
import httpretty
from httpretty.core import HTTPrettyRequest

PORT = '8756'
PATH = '/tests/resources/'


class SimpleHandler(CGIHTTPRequestHandler):
    def do_HEAD(self) -> None:
        if 'key' in self.requestline or 'value' in self.requestline:
            self.send_response(http.HTTPStatus.OK)
            self.send_header("params", 'key:value')
            self.end_headers()
            return
        f = self.send_head()
        if f:
            f.close()


def start_serve():
    """This method allow us to launch a small http server for our tests."""
    server_address = ("", int(PORT))
    server = http.server.HTTPServer
    handler = SimpleHandler
    handler.cgi_directories = [""]

    httpd = server(server_address, handler)
    httpd.serve_forever()


class CustomServerHandler(http.server.BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header(
            'WWW-Authenticate', 'Basic realm="Demo Realm"')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        key = self.server.get_auth_key()

        ''' Present frontpage with user authentication. '''
        if self.headers.get('Authorization') is None:
            self.do_AUTHHEAD()

            response = {
                'success': False,
                'error': 'No auth header'
            }

            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        elif self.headers.get('Authorization') == 'Basic ' + str(key):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            response = {
                'path': self.path,
            }

            self.wfile.write(bytes(json.dumps(response), 'utf-8'))
        else:
            self.do_AUTHHEAD()

            response = {
                'success': False,
                'error': 'Invalid credentials'
            }

            self.wfile.write(bytes(json.dumps(response), 'utf-8'))


class CustomHTTPServer(http.server.HTTPServer):
    key = ''

    def __init__(self, address, handlerClass=CustomServerHandler):
        super().__init__(address, handlerClass)

    def set_auth(self, username, password):
        self.key = base64.b64encode(
            bytes('%s:%s' % (username, password), 'utf-8')).decode('ascii')

    def get_auth_key(self):
        return self.key


def start_auth_serve():
    server = CustomHTTPServer(('', int(PORT)))
    server.set_auth('user', 'pwd123456')
    server.serve_forever()


def start_mock_oauth2_serve(service: str):
    resource_dir = os.path.join(os.path.dirname(__file__), 'resources')
    service_uri = f'{service}'
    resource = "https://something.com/resources/test.txt"
    not_resource = "https://something.com/resources/not_here.txt"

    def download(request: HTTPrettyRequest, uri, headers):
        body = request.headers
        print()
        if '06b485119f019b90499bc08683be27cae85f2be5ad9a707989b79698a7f1bb22' \
                in body.get('Authorization'):
            return 200, headers, b'This is my awesome test.'
        with open(os.path.join(resource_dir, 'wrong_user.json')) as f:
            data = f.read()
        return 401, headers, data

    def not_found(request: HTTPrettyRequest, uri, headers):
        return 404, headers, 'File not found'

    httpretty.enable()
    httpretty.register_uri(httpretty.GET, resource, download)
    httpretty.register_uri(httpretty.GET, not_resource, not_found)


def stop_mock_oauth2_serve():
    httpretty.disable()
    httpretty.reset()
