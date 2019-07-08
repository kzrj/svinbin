# -*- coding: utf-8 -*-
from __future__ import unicode_literals

class XFrameOptionsHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Frame-Options'] = "allow-from localhost:3000"
        # Access-Control-Allow-Origin
        # response['Access-Control-Allow-Origin'] = "*"
        return response