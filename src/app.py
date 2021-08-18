from .common.config import get_conf
from tornado.ioloop import IOLoop
from tornado.web import Application
import tornado.httpserver as httpserver
from .route import urls


def main():
    settings = get_conf().get('tornado', {})
    app = Application(urls, **settings)
    server = httpserver.HTTPServer(app)
    server.bind(10001, '0.0.0.0')
    server.start(1)
    IOLoop.current().start()
