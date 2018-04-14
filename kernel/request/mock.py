import json
from requests import Response


class Mock:
    def __init__(self, content):
        self.response = Response()
        self.response.status_code = 200
        self.response._content = json.dumps(content).encode()

    def get(self, *args, **kwargs):
        return self.response

    def post(self, *args, **kwargs):
        return self.response

    def get_safe(self, *args, **kwargs):
        return self.response

    def post_safe(self, *args, **kwargs):
        return self.response
