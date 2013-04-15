#!/usr/bin/env python

import unittest
from pybrowsertest import *

class AutomationTest(BrowserTestCase):
    def test_the_title_is_set(self):
        self.assertEquals("Directory listing for /", self.browser.open('').title)

    def test_there_are_links(self):
        links = self.browser.open('').find_elements_by_css_selector('a')
        self.assertTrue(len(list(links)) > 0)

    def test_fail_test(self):
        self.assertEquals("This test should fail", self.browser.open('').title)


class AWidgetTest(BrowserTestCase):
    def test_has_href_attribute(self):
        link = self.browser.open('').find_elements_by_css_selector('a').next()
        self.assertIsInstance(link.href, unicode)


class BodyWidgetTest(BrowserTestCase):
    def test_body(self):
        body = self.browser.open('').find_element_by_tag_name('body')
        self.assertIsNotNone(body)


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
