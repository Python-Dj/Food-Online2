from . import models

class RequestObjectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        models.request_obj = request

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response