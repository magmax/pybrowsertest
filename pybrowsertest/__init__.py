#!/usr/bin/python
# -*- mode:python; coding:utf-8; tab-width:4 -*-

# This file is part of pybrowsertest
#
# Pybrowsertest is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pybrowsertest is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import unittest
import time
from functools import partial

from ConfigParser import ConfigParser
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from widgets import *

__all__ = [
    'BrowserTestCase',
    'onlyIfBrowserIn', 'onlyIfBrowserNotIn'
    ]


def featuredAddFailure(original):
    def addFailure(self, test, err):
        test.saveScreenshot()
        return original(test, err)
    return addFailure


class BrowserConfiguration(object):
    SECTION_GLOBAL = 'global'
    SECTION_DESIRED = 'desired capabilities'

    OPTION_SELENIUM_MODE = 'selenium_mode'
    OPTION_SELENIUM_URL = 'selenium_url'
    OPTION_TESTING_URL = 'testing_url'
    OPTION_SCREENSHOT_PATTERN = 'screenshot_file_pattern'
    OPTION_BROWSER_NAME = 'browserName'
    OPTION_JAVASCRIPT = 'javascriptEnabled'

    default_selenium_url = 'http://localhost:4444/wd/hub'
    default_selenium_mode = 'remote'
    default_testing_url = 'http://localhost'
    default_screenshot_pattern = 'error.{testname}.{timestamp}.png'

    default_browser_name = 'firefox'
    default_javascript = True

    def __init__(self):
        self._config = ConfigParser()
        self._config.optionxform = str
        self._config.add_section(self.SECTION_GLOBAL)
        self._config.set(self.SECTION_GLOBAL, self.OPTION_SELENIUM_URL, self.default_selenium_url)
        self._config.set(self.SECTION_GLOBAL, self.OPTION_SELENIUM_MODE, self.default_selenium_mode)
        self._config.set(self.SECTION_GLOBAL, self.OPTION_TESTING_URL, self.default_testing_url)
        self._config.set(self.SECTION_GLOBAL, self.OPTION_SCREENSHOT_PATTERN, self.default_selenium_mode)

        self._config.add_section(self.SECTION_DESIRED)
        self._config.set(self.SECTION_DESIRED, self.OPTION_BROWSER_NAME, self.default_browser_name)
        self._config.set(self.SECTION_DESIRED, self.OPTION_JAVASCRIPT, self.default_javascript)

    def loadDefaultFiles(self):
        self.load(['/etc/browsertest.cfg', '.browsertest.cfg', 'browsertest.cfg'])

    def load(self, filelist):
        for filename in filelist:
            if os.path.exists(filename):
                self._config.read(filename)

    @property
    def selenium_mode(self):
        return self._config.get(self.SECTION_GLOBAL, self.OPTION_SELENIUM_MODE)

    @property
    def selenium_url(self):
        return self._config.get(self.SECTION_GLOBAL, self.OPTION_SELENIUM_URL)

    @property
    def testing_url(self):
        return self._config.get(self.SECTION_GLOBAL, self.OPTION_TESTING_URL)

    @property
    def screenshot_file_pattern(self):
        return self._config.get(self.SECTION_GLOBAL, self.OPTION_SCREENSHOT_PATTERN)

    @property
    def browser_name(self):
        return self._config.get(self.SECTION_DESIRED, self.OPTION_BROWSER_NAME)

    @property
    def desired_capabilities(self):
        desired = {}
        for option in self._config.options(self.SECTION_DESIRED):
            desired[option] = self._config.get(self.SECTION_DESIRED, option)
        return desired


class DriverFactory(object):
    @classmethod
    def make(cls, config):
        drivers = {
            'remote': partial(webdriver.Remote,
                              config.selenium_url,
                              config.desired_capabilities),
            'firefox': webdriver.Firefox,
            'chrome': webdriver.Chrome
            }
        return drivers[config.selenium_mode]()


class Browser(object):
    def __init__(self, config):
        self._config = config
        self._driver = None
        self._driver = DriverFactory.make(config)

    def __del__(self):
        self.close()

    def open(self, url):
        full_url = self._config.testing_url + url
        self._driver.get(full_url)
        return Page(self._driver, full_url)

    def close(self):
        if self._driver:
            self._driver.close()
            self._driver = None


class BrowserTestCase(unittest.TestCase):
    _config = BrowserConfiguration()
    _config.loadDefaultFiles()
    _browsers = []

    def __init__(self, *args, **kargs):
        unittest.TestCase.__init__(self, *args, **kargs)

    def run(self, result=None):
        if result is None:
            result = self.defaultTestResult()
        if result.addFailure != featuredAddFailure:
            func_type = type(result.addFailure)
            result.addFailure = func_type(featuredAddFailure(result.addFailure), result, unittest.TestResult)

        return unittest.TestCase.run(self, result)

    def saveScreenshot(self):
        try:
            for driver in self._browsers:
                if hasattr(driver, 'save_screenshot'):
                    filename = self._config.screenshot_file_pattern.format(testname=self.id(), timestamp=time.time())
                    driver.save_screenshot(filename)
        except Exception as e:
            print "BROWSER_FRAMEWORK EXCEPTION: ", e.message

    @property
    def browser(self):
        retval = Browser(self._config)
        self.addCleanup(retval.close)
        self._browsers.append(retval)
        return retval


def onlyIfBrowserIn(*browserNames):
    config = BrowserConfiguration()
    config.loadDefaultFiles()
    message = 'The test has been skipped for browser: {}'
    return unittest.skipIf(config.browser_name not in browserNames, message.format(browserNames))

def onlyIfBrowserNotIn(*browserNames):
    config = BrowserConfiguration()
    config.loadDefaultFiles()
    message = 'Current browser {} does not match any required browser for this test: {}'
    return unittest.skipIf(config.browser_name in browserNames, message.format(config.browser_name, browserNames))
