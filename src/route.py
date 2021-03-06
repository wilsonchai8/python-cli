from .common.web_handler import WebHandler, HTTPError


class TestFlow(WebHandler):
    def post(self, *args, **kwargs):
        data = self.get_request_body_json()
        self.reply(data=data)

    def get(self, *args, **kwargs):
        query = self.get_request_query_json()
        self.reply(data=query)


class NotFoundHandler(WebHandler):
    def prepare(self):
        raise HTTPError(status_code=404, log_message=self.request.uri)

urls = [
    (r'/test', TestFlow),
]

# append in ths last
urls.append(
    (r'/.*', NotFoundHandler),
)