#!/usr/bin/env python

# In order to test this file, you only need a selenium server
# and a server created with:
#   $ python -m SimpleHTTPServer
# Then you can use:
#   $ nosetests examples/generic.py
# It has a failing test, a skipped one and two right tests

import unittest
from pybrowsertest import BrowserTestCase

class AutomationTest(BrowserTestCase):
    def test_the_title_is_set(self):
        browser = self.getBrowser()
        self.assertEquals("Directory listing for /", browser.title)

    def test_there_are_links(self):
        browser = self.getBrowser()
        links = browser.find_elements_by_css_selector('a')
        self.assertTrue(len(links) > 0)

    def test_failing_test(self):
        browser = self.getBrowser()
        self.assertEquals("This test should fail", browser.title)

    @unittest.skip("This test should not be executed ever")
    def test_skipped_test(self):
        browser = self.getBrowser()
        self.fail("This test should not be executed")
