from blinker import Namespace
from .signals import http_response_signal, http_request_signal

_namespace = Namespace()


def get_anonymous_event(name):
    return _namespace.signal(name=name)
