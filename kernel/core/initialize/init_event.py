from flask import request
from kernel.signal import http_request_signal, http_response_signal


def init_event(core):
    app = core.app
    app.before_request(_before_each_request)
    app.after_request(_after_each_request)


def _before_each_request():
    http_request_signal.send(request=request)


def _after_each_request(response):
    http_response_signal.send(response=response)
    return response
