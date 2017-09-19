import json
import os
import logging
import re
from string import Template
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado_json.requesthandlers import APIHandler
from unipath import Path
from tornado_json import schema

from hash import generate

STATIC_PATH = Path(Path(__file__).parent, 'static')
WORKER_PATH = Path(Path(__file__).parent, '')


class MainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        super(MainHandler, self).set_default_headers()

        # Allow cross-origin Ajax requests (CORS)
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @classmethod
    def setup(cls):
        logging.basicConfig(level=logging.WARNING)
        logger = logging.getLogger('hashing')
        logger.propagate = False
        logger.setLevel(logging.WARNING)
        handler = logging.StreamHandler()
        logger.addHandler(handler)
        return logger

    def prepare(self):
        if ('X-Forwarded-Proto' in self.request.headers and
                    self.request.headers['X-Forwarded-Proto'] != 'https'):
            self.redirect(re.sub(r'^([^:]+)', 'https', self.request.full_url()))

    def get(self):
        self.get_landing_page()
        return

    def get_landing_page(self):
        with open('index.html', 'r') as f:
            html_template = f.read()
            html = Template(html_template).safe_substitute({
                'paycoin': '',
            })
            self.write(html)


class HashHandler(APIHandler):
    HASH_ACTIONS = ['encrypt', 'decrypt']

    @classmethod
    def setup(cls):
        logging.basicConfig(level=logging.WARNING)
        logger = logging.getLogger('hashing')
        logger.propagate = False
        logger.setLevel(logging.WARNING)
        handler = logging.StreamHandler()
        logger.addHandler(handler)
        return logger

    def set_default_headers(self):
        super(HashHandler, self).set_default_headers()
        # Allow cross-origin Ajax requests (CORS)
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def prepare(self):
        if ('X-Forwarded-Proto' in self.request.headers and
                    self.request.headers['X-Forwarded-Proto'] != 'https'):
            self.redirect(re.sub(r'^([^:]+)', 'https', self.request.full_url()))

    @schema.validate(
        input_schema={
            'title': 'HashObject',
            'type': 'object',
            'properties': {
               'message': {'type': 'string'},
               'password': {'type': 'string'},
               'phrase': {'type': 'string'},
               'action': {'type': 'string',
                          'enum': ['decrypt', 'encrypt']}
            },
            'required': ['message', 'password',
                         'phrase', 'action']
        },
        input_example={
            'message': 'Very Important Post-It Note',
            'password': 'Equally important message',
            'phrase': '1221',
            'action': 'decrypt'
        },
        output_schema={
            'type': 'object',
            'properties': {
                'key': {'type': 'string'}
            }
        },
        output_example={
            'key': 'Very Important Post-It Note was posted.'
        },
    )
    def post(self):
        client_obj = json.loads(self.request.body)
        logger = logging.getLogger('hashing')
        logger.info('Request body value={}'.format(client_obj))
        response_obj = generate(message=client_obj['message'],
                                password=client_obj['password'],
                                salt=client_obj['phrase'],
                                action=client_obj['action'])
        return response_obj


def main():
    MainHandler.setup()
    application = tornado.web.Application([
        (r'/', MainHandler),
        (r'/hash', HashHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': STATIC_PATH}),
        (r'/(service-worker.js)', tornado.web.StaticFileHandler,
         {'path': WORKER_PATH}),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get('PORT', 5000))
    http_server.xheaders = True
    http_server.bind(port)
    http_server.start(1)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
