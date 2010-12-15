from django.test import TestCase
from sugar.templatetags.pygment_tags import pygmentize
from sugar.middleware.cors_middleware import CORSMiddleware

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


class CORSTests(self):

    def json_test(self):
        cors = CORSMiddleware()

