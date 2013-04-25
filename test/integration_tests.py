# -*- mode:python; coding:utf-8; tab-width:4 -*-

import string

from hamcrest import contains_string

from prego import TestCase, Task
from prego.net import localhost, listen_port


CONFIG_TEMPLATE = """
[global]
testing_url = http://localhost:8000
screenshot_file_pattern = error.{testname}.{timestamp}.png
selenium_mode = ${selenium_mode}
selenium_url = http://localhost:4444/wd/hub

[desired capabilities]
browser_name = ${browser}
javascript_enabled = True
"""


def write_config_file(mode, browser=None):
    browser = browser or mode
    template = string.Template(CONFIG_TEMPLATE)
    with file('browsertest.cfg', 'w') as fd:
        fd.write(template.safe_substitute(browser=browser, selenium_mode=mode))


firefox_skips = [
    'test_skip_test (tests.SkippingTest) ... SKIP',
    'test_skipif_browser_is_firefox (tests.SkippingTest) ... SKIP',
    'test_skipifnot_foo (tests.SkippingTest) ... SKIP']

chrome_skips = [
    "test_skip_test (tests.SkippingTest) ... SKIP",
    "test_skipifnot_browser_is_not_firefox (tests.SkippingTest) ... SKIP",
    "test_skipifnot_foo (tests.SkippingTest) ... SKIP"]


class Tests(TestCase):
    def run_with_config(self, mode, browser=None):
        write_config_file(mode, browser)

        server = Task(detach=True)
        server.command('python -m SimpleHTTPServer 8000', expected=-15, timeout=None)

        tester = Task()
        tester.wait_that(localhost, listen_port(8000))
        tester.command('nosetests -v test/tests.py', timeout=60)

        Task().command('killall chromedriver', expected=None, timeout=None)
        return tester

    def start_selenium_server(self):
        Se = Task(detach=True)
        Se.command('java -jar selenium-server-standalone-2.31.0.jar',
                   expected=143, timeout=None)
        Task().wait_that(localhost, listen_port(4444))

    def assert_skips(self, task, skips):
        for line in skips:
            task.assert_that(task.lastcmd.stderr.content, contains_string(line))

    def test_local_chrome(self):
        tester = self.run_with_config('chrome')
        self.assert_skips(tester, chrome_skips)

    def test_local_firefox(self):
        tester = self.run_with_config('firefox')
        self.assert_skips(tester, firefox_skips)

    def test_remote_firefox(self):
        self.start_selenium_server()
        tester = self.run_with_config('remote', 'firefox')
        self.assert_skips(tester, firefox_skips)
