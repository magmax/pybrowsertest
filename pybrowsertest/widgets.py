#!/usr/bin/python
# -*- mode:python; coding:utf-8; tab-width:4 -*-

class Container(object):
    def __init__(self, driver):
        self._driver = driver

    def find_elements_by_css_selector(self, selector):
        for element in self._driver.find_elements_by_css_selector(selector):
            yield ElementFactory.make(self._driver, element)

    def find_element_by_tag_name(self, name):
        element = self._driver.find_element_by_tag_name(name)
        return ElementFactory.make(self._driver, element) if element else None


class Widget(Container):
    def __init__(self, driver, element):
        Container.__init__(self, driver)
        self._element = element
        self.get_attribute = self._element.get_attribute

class AWidget(Widget):
    @property
    def href(self):
        return self.get_attribute('href')

    @property
    def target(self):
        return self.get_attribute('target')

    @property
    def title(self):
        return self.get_attribute('title')


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
