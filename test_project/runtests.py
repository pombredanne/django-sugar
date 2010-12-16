# See
# http://ericholscher.com/blog/2009/jun/29/enable-setuppy-test-your-django-apps/
# http://gremu.net/blog/2010/enable-setuppy-test-your-django-apps/

import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'
test_dir = os.path.dirname(__file__)
sys.path.insert(0, test_dir)

from django.test.utils import get_runner
from django.conf import settings

def runtests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=0, interactive=False)
    failures = test_runner.run_tests(['sugar'])
    sys.exit(bool(failures))

if __name__ == '__main__':
    runtests()