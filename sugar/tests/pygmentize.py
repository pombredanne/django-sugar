import re

from django.test.testcases import TestCase

from sugar.templatetags.pygment_tags import pygmentize

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
