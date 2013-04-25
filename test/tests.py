#!/usr/bin/env python

import unittest
from pybrowsertest import *

EXAMPLE1 = '/test/html/example1.html'
EXAMPLE_FORMS = '/test/html/example_forms.html'


class AutomationTest(BrowserTestCase):
    def test_the_title_is_set(self):
        self.assertEquals("Directory listing for /", self.browser.open('').title)

    def test_there_are_links(self):
        links = self.browser.open('').find_elements_by_css_selector('a')
        self.assertTrue(len(list(links)) > 0)


class AWidgetTest(BrowserTestCase):
    def test_has_href_attribute(self):
        link = self.browser.open(EXAMPLE1).find_elements_by_css_selector('a').next()
        self.assertIsInstance(link.href, unicode)
        self.assertTrue(link.href.endswith('/link1'))
        self.assertEquals('_blank', link.target)


class PWidgetTest(BrowserTestCase):
    def test_paragraph(self):
        par = self.browser.open(EXAMPLE1).find_elements_by_css_selector('p').next()
        self.assertIsNotNone(par)


class RetrievingWidgetsTest(BrowserTestCase):
    def test_inmediate(self):
        page = self.browser.open(EXAMPLE1)
        page.find_element('btn-create').click()
        with self.assertRaises(Exception):
            item = page.find_element('created')

    def test_retrieving_after_a_timeout(self):
        page = self.browser.open(EXAMPLE1)
        page.find_element('btn-create').click()
        item = page.find_element('created', timeout=5000)
        self.assertIsNotNone(item)


class FormUsageTest(BrowserTestCase):
    def setUp(self):
        self.page = self.browser.open(EXAMPLE_FORMS)

    def test_form_item(self):
        form = self.page.find_element_by_tag_name('form')
        self.assertEqual('get', form.method)
        self.assertIn('the_action', form.action)

    def test_item_can_be_cleared(self):
        textitem = self.page.find_element('text-item')
        textitem.clear()

        self.assertEqual('', textitem.value)

    def test_item_can_be_written(self):
        text = 'The world is a vampire, send to drain'
        textitem = self.page.find_element('text-item')
        textitem.clear()
        textitem.send_keys(text)

        self.assertEqual(text, textitem.value)

    def test_textarea_can_be_cleared(self):
        textitem = self.page.find_element_by_tag_name('textarea')
        textitem.clear()

        self.assertEqual('', textitem.value)

    def test_textarea_value_can_be_set(self):
        textitem = self.page.find_element_by_tag_name('textarea')
        textitem.value = "Text 1"
        textitem.value = "Text 2"

        self.assertEqual('Text 2', textitem.value)


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
