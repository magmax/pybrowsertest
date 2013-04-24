#!/usr/bin/python
# -*- mode:python; coding:utf-8; tab-width:4 -*-

# This file is part of pybrowsertest
#
# Pybrowsertest is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pybrowsertest is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from functools import partial

class Container(object):
    def __init__(self, driver):
        self._driver = driver
        self.find_element = partial(self._find_element, self._driver.find_element_by_id)
        self.find_element_by_css_selector = partial(self._find_element, self._driver.find_element_by_css_selector)
        self.find_elements_by_css_selector = partial(self._find_elements, self._driver.find_elements_by_css_selector)
        self.find_element_by_xpath = partial(self._find_element, self._driver.find_element_by_xpath)
        self.find_elements_by_xpath = partial(self._find_elements, self._driver.find_elements_by_xpath)
        self.find_element_by_tag_name = partial(self._find_element, self._driver.find_element_by_tag_name)
        self.find_elements_by_tag_name = partial(self._find_elements, self._driver.find_elements_by_tag_name)
        self.find_element_by_class_name = partial(self._find_element, self._driver.find_element_by_class_name)
        self.find_elements_by_class_name = partial(self._find_elements, self._driver.find_elements_by_class_name)

    def _find_element(self, function, selector, timeout=None):
        try:
            if timeout:
                self._driver.implicitly_wait(timeout)
            element = function(selector)
            return ElementFactory.make(self._driver, element) if element else None
        finally:
            if timeout:
                self._driver.implicitly_wait(0)

    def _find_elements(self, function, selector):
        for element in function(selector):
            yield ElementFactory.make(self._driver, element)


class Widget(Container):
    def __init__(self, driver, element):
        Container.__init__(self, driver)
        self._element = element

        # properties
        self.id = self._element.id
        self.text = self._element.text
        self.size = self._element.size
        self.get_attribute = self._element.get_attribute
        self.tag_name = self._element.tag_name
        self.location = self._element.location

        # booleans
        self.is_displayed = self._element.is_displayed
        self.is_enabled = self._element.is_enabled

        # actions
        self.click = self._element.click

        # other
        self.__str__ = self._element.__str__


class AWidget(Widget):
    @property
    def href(self):
        return self.get_attribute('href')

    @property
    def target(self):
        return self.get_attribute('target')


class InputWidget(Widget):
    @property
    def type(self):
        return self.get_attribute('type')

    @property
    def value(self):
        return self.get_attribute('value')

    @value.setter
    def value(self, value):
        self._element.clear()
        self._element.send_keys(value)
        return self._element

    @property
    def placeholder(self):
        return self.get_attribute('placeholder')

    def clear(self):
        self._element.clear()
        return self._element

    def is_selected(self):
        return self._element.is_selected()

    def send_keys(self, keys):
        return self._element.send_keys(keys)


class TextareaWidget(Widget):
    @property
    def value(self):
        return self.get_attribute('value')

    @value.setter
    def value(self, value):
        self._element.clear()
        self._element.send_keys(value)
        return self._element

    @property
    def rows(self):
        return self.get_attribute('rows')

    @property
    def placeholder(self):
        return self.get_attribute('placeholder')

    def clear(self):
        self._element.clear()
        return self._element

    def send_keys(self, keys):
        return self._element.send_keys(keys)


class FormWidget(Widget):
    @property
    def method(self):
        return self.get_attribute('method')

    @property
    def action(self):
        return self.get_attribute('action')

    def submit(self):
        return self._element.submit()


class ElementFactory(object):
    ELEMENTS = {
        'a': AWidget,
        'input': InputWidget,
        'textarea': TextareaWidget,
        'form': FormWidget,
        }
    @classmethod
    def make(cls, driver, element):
        if element.tag_name in cls.ELEMENTS:
            return cls.ELEMENTS[element.tag_name](driver, element)
        return Widget(driver, element)


class Page(Container):
    def __init__(self, driver, url):
        Container.__init__(self, driver)
        self._url = url
        self.get_screenshot_as_file = self._driver.get_screenshot_as_file
        self.get_screenshot_as_base64 = self._driver.get_screenshot_as_base64
        self.current_url = self._driver.current_url

    @property
    def title(self):
        return self._driver.title
