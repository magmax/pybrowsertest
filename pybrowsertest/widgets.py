#!/usr/bin/python
# -*- mode:python; coding:utf-8; tab-width:4 -*-

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


class ElementFactory(object):
    ELEMENTS = {
        'a': AWidget,
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
