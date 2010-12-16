from django.conf import settings
from django.test.testcases import TestCase
from django.http import HttpRequest, HttpResponse

from sugar.middleware.cors import CORSMiddleware


class CORSTests(TestCase):

    def test_middleware(self):
        cors = CORSMiddleware()
        request = HttpRequest()
        request.path = "/"

        response = HttpResponse('["foo"]',
                                mimetype='application/json')

        cors.process_response(request, response)

        self.assertEqual(response['access-control-allow-origin'], '*')

    def test_non_interference(self):
        "CORS Middleware shouldn't touch responses outside of its mimetypes"
        cors = CORSMiddleware()

        request = HttpRequest()
        request.path = "/cicero"

        response = HttpResponse('Lorem ipsum dolor sit amet',
                                mimetype='text/html')

        cors.process_response(request, response)

        self.assertFalse(response.has_header('access-control-allow-origin'))

    def test_custom_settings(self):
        "CORS Middleware shouldn't touch responses outside of its mimetypes"

        settings.CORS_PATHS = (
            ('/foo', ('application/json', ), (('Access-Control-Allow-Origin', 'foo.example.com'), )),
            ('/bar', ('application/json', ), (('Access-Control-Allow-Origin', 'example.com'), )),
            ('/', ('application/json', ), (('Access-Control-Allow-Origin', '*'), )),
        )


        cors = CORSMiddleware()

        request = HttpRequest()
        request.path = "/test"

        response = HttpResponse('["foo"]', mimetype='application/json')
        cors.process_response(request, response)
        self.assertEqual(response['access-control-allow-origin'], '*')

        request.path = "/foo/bar/baaz/quux"
        cors.process_response(request, response)
        self.assertEqual(response['access-control-allow-origin'], 'foo.example.com')

        request.path = "/bar/baaz/quux"
        cors.process_response(request, response)
        self.assertEqual(response['access-control-allow-origin'], 'example.com')

