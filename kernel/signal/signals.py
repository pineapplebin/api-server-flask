from blinker import Signal


class HttpRequestSignal(Signal):
    def send(self, *sender, request):
        super().send(*sender, request=request)


class HttpResponseSignal(Signal):
    def send(self, *sender, response):
        super().send(*sender, response=response)


http_request_signal = HttpRequestSignal()
http_response_signal = HttpResponseSignal()
