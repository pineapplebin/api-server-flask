import json
from flask import current_app, g
from kernel.signal import http_response_signal, http_request_signal
from kernel.utils import jsonformat, randomstr


@http_request_signal.connect
def each_request(sender, request):
    g.request_id = randomstr(10, 'both')
    current_app.logger.info(jsonformat(
        request_id=g.request_id,
        url=request.url,
        query=request.args,
        data=request.json or request.form))


@http_response_signal.connect
def each_response(sender, response):
    from flask import request
    request_id = g.get('request_id', None)
    if response.status_code != 200:
        return current_app.logger.warn(jsonformat(
            request_id=request_id,
            url=request.url,
            status_code=response.status_code))
