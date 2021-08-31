from tornado.web import RequestHandler, HTTPError
from .log_handler import logger, access_logger
import traceback
import json
from .const import *
from .exception_handler import ParamError

class WebHandler(RequestHandler):

    def initialize(self):
        pass

    def prepare(self):
        pass

    def on_finish(self):
        access_logger.info('{} {} {} {} {} {}ms'.format(
            self.request.protocol,
            self._status_code,
            self.request.method,
            self.request.uri,
            '-' if not self.request.body else self.request.body.decode('utf-8'),
            float(str(self.request.request_time()*1000)[0:5])))

    def write_error(self, status_code, **kwargs):
        if 'exc_info' in kwargs: 
            code = 2 if ParamError in kwargs.get('exc_info') else 1
            self.reply(MSGS.get(code), code, status_code)
        else:
            self.reply(self.reason, 1, status_code)

    def reply(self, msg=None, code=SUCCESS, status_code=200, **kwargs):
        res = {
            'code': code,
            'msg': MSGS.get(code) if not msg else msg
        }
        res.update(kwargs)
        self.set_status(status_code)
        self.finish(res)

    def log_exception(self, typ, value, tb):
        logger.error(traceback.format_exc())

    def get_request_query_json(self):
        ret = {}
        if self.request.arguments:
            for name, values in self.request.query_arguments.items():
                if len(values) == 1:
                    if values[0] != b'':
                        ret[name] = values[0].decode()
                else:
                    ret[name] = [i.decode() for i in values]
        return ret

    def get_request_body_json(self):
        ret = {}
        if self.request.body:
            try:
                data = json.loads(self.request.body.decode('utf-8'))
            except json.JSONDecodeError:
                raise ParamError('body json decode error')
            for name, values in data.items():
                ret[name] = values
        return ret
