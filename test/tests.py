#!/usr/bin/env python

import unittest
from pybrowsertest import *

EXAMPLE1 = '/test/html/example1.html'
EXAMPLE_FORMS = '/test/html/example_forms.html'


class AutomationTest(BrowserTestCase):
    def test_page_is_retrieved(self):
        page = self.browser.open('')

        self.assertEquals("Directory listing for /", page.title)
        self.assertTrue(len(list(page.find_elements_by_css_selector('a'))) > 0)


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
    def setUp(self):
        self.page = self.browser.open(EXAMPLE1)
    def test_inmediate(self):
        self.page.find_element('btn-create').click()
        with self.assertRaises(Exception):
            item = self.page.find_element('created')

    def test_retrieving_after_a_timeout(self):
        self.page.find_element('btn-create').click()
        item = self.page.find_element('created', timeout=5000)
        self.assertIsNotNone(item)

    def test_can_find_an_item_inside_another(self):
        ul = self.page.find_element_by_css_selector('ul')
        li_list = list(ul.find_elements_by_css_selector('li'))
        self.assertEqual('item 1', li_list[0].text)
        self.assertEqual('item 2', li_list[1].text)


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
    def test_onlyifbrowserin_firefox(self):
        pass

    @onlyIfBrowserIn("invalid browser")
    def test_onlyifbrowserin_foo(self):
        self.fail("This test should not be executed")

    @onlyIfBrowserNotIn("firefox")
    def test_onlyifbrowsernotin_firefox(self):
        pass
