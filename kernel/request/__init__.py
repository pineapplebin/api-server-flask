import requests
import json
from flask import current_app
from kernel.utils import jsonformat
from .mock import Mock


def _request_log(**kwargs):
    current_app.logger.info(jsonformat(_msg='Remote request', **kwargs))


class Requester:
    def _request(self, method, url, **kwargs):
        _request_log(url=url, **kwargs)
        return getattr(requests, method)(url, **kwargs)

    def get(self, url, *, params=None, **kwargs) -> requests.Response:
        return self._request('get', url, params=params, **kwargs)

    def post(self, url, *, data, params=None, **kwargs) -> requests.Response:
        return self._request('post', url, data=data, params=params, **kwargs)

    def _request_safe(self, method, **kwargs):
        try:
            return self._request(method, **kwargs)
        except Exception as e:
            current_app.logger.error(jsonformat(error=str(e)))
            return None

    def get_safe(self, url, *, params=None, **kwargs) -> requests.Response:
        return self._request_safe('get', url=url, params=params, **kwargs)

    def post_safe(self, url, *, data, params=None,
                  **kwargs) -> requests.Response:
        return self._request_safe('post', url=url, data=data, params=params,
                                  **kwargs)

    def parse(self, res: requests.Response):
        try:
            rst = json.loads(res.content.decode('utf8'))
            return rst
        except json.JSONDecodeError:
            return res.content.decode('utf8')

    def mock(self, response) -> Mock:
        return Mock(response)


requester = Requester()
