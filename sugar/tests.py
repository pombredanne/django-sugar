import re

from django.conf import settings
from django.test.testcases import TestCase
from django.http import HttpRequest, HttpResponse

from sugar.templatetags.pygment_tags import pygmentize
from sugar.middleware.cors import CORSMiddleware

class PygmentTagsTestCase(TestCase):
    def _html_stripper(self, input):
        """Quick and dirty HTML tag stripper & whitespace cleaner not intended
        for serious use"""
        return re.sub('\s+', ' ', re.sub('<[^>]+>', '', input)).strip()

    def test_none(self):
        text = u'This is a test'
        self.assertEqual(text, pygmentize(text))

    def test_default(self):
        input = u'<code>a = 6</code>'
        output = pygmentize(input)
        self.assertNotEqual(input, output)
        self.assertEqual(self._html_stripper(input), self._html_stripper(output))

    def test_class_python(self):
        input = u'<code class="python">foo = str(6)</code>'
        output = pygmentize(input)

        self.assertNotEqual(input, output)
        self.assertEqual(self._html_stripper(input), self._html_stripper(output))

        # Hackish but effective:
        self.assertTrue('<span class="nb">str</span>' in output)

    def test_class_js(self):
        input = u'<code class="javascript">var foo = 6.toString();</code>'
        output = pygmentize(input)
        self.assertNotEqual(input, output)
        self.assertEqual(self._html_stripper(input), self._html_stripper(output))

        # Hackish but effective:
        self.assertTrue('<span class="nx">toString</span>' in output)


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

