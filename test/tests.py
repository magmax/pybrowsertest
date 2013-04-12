#!/usr/bin/env python

import unittest
from pybrowsertest import *

class AutomationTest(BrowserTestCase):
    def foo(self):
        pass

    def test_the_title_is_set(self):
        browser = self.getBrowser('')
        self.assertEquals("Directory listing for /", browser.title)

    def test_there_are_links(self):
        browser = self.getBrowser('')
        links = browser.find_elements_by_css_selector('a')
        self.assertTrue(len(links) > 0)

    def test_fail_test(self):
        browser = self.getBrowser('')
        self.assertEquals("This test should fail", browser.title)


class SkippingTest(BrowserTestCase):
    def foo(self):
        pass

    @unittest.skip("This test should not be executed ever")
    def test_skip_test(self):
        self.fail("This test should not be executed")

    @onlyIfBrowserIn("firefox")
    def test_skipifnot_browser_is_not_firefox(self):
        pass

    @onlyIfBrowserIn("invalid browser")
    def test_skipifnot_foo(self):
        self.fail("This test should not be executed")

    @onlyIfBrowserNotIn("firefox")
    def test_skipif_browser_is_firefox(self):
        pass
