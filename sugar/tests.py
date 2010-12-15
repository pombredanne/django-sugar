from django.http import HttpRequest, HttpResponse
from django.test import TestCase

from sugar.templatetags.pygment_tags import pygmentize
from sugar.middleware.cors import CORSMiddleware

class PygmentTagsTestCase(TestCase):
    
    def testNone(self):
        text = u'This is a test'
        self.assertEqual(text, pygmentize(text))
    
    def testDefault(self):
        text = u'<code>a = 6</code>'
        self.assertNotEqual(text, pygmentize(text))
        
    def testElement(self):
        text = u'<pre>a = 6</pre>'
        self.assertNotEqual(text, pygmentize(text, 'pre'))
        self.assertEqual(text, pygmentize(text, 'pre:foo'))
        
    def testElementClass(self):
        text = u'<pre class="foo">a = 6</pre>'
        self.assertEqual(text, pygmentize(text, 'pre'))
        self.assertNotEqual(text, pygmentize(text, 'pre:foo'))


class CORSTests():

    def json_test(self):
        cors = CORSMiddleware()
        request = HttpRequest()
        response = HttpResponse('["foo"]',
                mimetype='application/json')
        cors.process_response(request, response)
        self.assertEqual(response.get('Access-Control-Allow-Origin', '*'))
