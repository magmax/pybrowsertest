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
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from functools import partial

class Container(object):
    def __init__(self, driver):
        self._driver = driver
        self.find_element_by_css_selector = partial(self._find_element, self._driver.find_element_by_css_selector)
        self.find_elements_by_css_selector = partial(self._find_elements, self._driver.find_elements_by_css_selector)
        self.find_element_by_xpath = partial(self._find_element, self._driver.find_element_by_xpath)
        self.find_elements_by_xpath = partial(self._find_elements, self._driver.find_elements_by_xpath)
        self.find_element_by_tag_name = partial(self._find_element, self._driver.find_element_by_tag_name)
        self.find_elements_by_tag_name = partial(self._find_elements, self._driver.find_elements_by_tag_name)
        self.find_element_by_class_name = partial(self._find_element, self._driver.find_element_by_class_name)
        self.find_elements_by_class_name = partial(self._find_elements, self._driver.find_elements_by_class_name)

    def _find_element(self, function, selector):
        element = function(selector)
        return ElementFactory.make(self._driver, element) if element else None

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

    @property
    def placeholder(self):
        return self.get_attribute('placeholder')


class TextareaWidget(Widget):
    @property
    def rows(self):
        return self.get_attribute('rows')

    @property
    def placeholder(self):
        return self.get_attribute('placeholder')


class ElementFactory(object):
    ELEMENTS = {
        'a': AWidget,
        'input': InputWidget,
        'textarea': TextareaWidget,
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

    @property
    def title(self):
        return self._driver.title
