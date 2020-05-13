# -*- coding: utf-8 -*-


class XFrameOptionsHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Frame-Options'] = "allow-from localhost:3000"

        return response