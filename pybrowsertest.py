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
from ConfigParser import ConfigParser
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

__all__ = [
    'BrowserTestCase',
    'avoidInBrowsers', 'unlessInBrowsers',
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

    def __init__(self):
        self._config = ConfigParser()
        self._config.optionxform = str
        self._config.add_section(self.SECTION_GLOBAL)
        self._config.set(self.SECTION_GLOBAL, self.OPTION_SELENIUM_URL, 'http://localhost:4444/wd/hub')
        self._config.set(self.SECTION_GLOBAL, self.OPTION_SELENIUM_MODE, 'remote')
        self._config.set(self.SECTION_GLOBAL, self.OPTION_TESTING_URL, 'http://localhost')
        self._config.set(self.SECTION_GLOBAL, self.OPTION_SCREENSHOT_PATTERN, 'error.{testname}.{timestamp}.png')

        self._config.add_section(self.SECTION_DESIRED)
        self._config.set(self.SECTION_DESIRED, self.OPTION_BROWSER_NAME, 'firefox')
        self._config.set(self.SECTION_DESIRED, self.OPTION_JAVASCRIPT, 'true')

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


class BrowserTestCase(unittest.TestCase):
    def __init__(self, *args, **kargs):
        unittest.TestCase.__init__(self, *args, **kargs)

        self._drivers = []
        self._config = BrowserConfiguration()
        self._config.loadDefaultFiles()

    def run(self, result=None):
        if result is None:
            result = self.defaultTestResult()
        if result.addFailure != featuredAddFailure:
            func_type = type(result.addFailure)
            result.addFailure = func_type(featuredAddFailure(result.addFailure), result, unittest.TestResult)

        return unittest.TestCase.run(self, result)

    def saveScreenshot(self):
        try:
            if len(self._drivers) != 0 and hasattr(self._drivers[0], 'save_screenshot'):
                filename = self._config.screenshot_file_pattern.format(testname=self.id(), timestamp=time.time())
                self._drivers[0].save_screenshot(filename)
        except Exception as e:
            print "BROWSER_FRAMEWORK EXCEPTION: ", e.message

    def getBrowser(self, url=''):
        if len(self._drivers) == 0:
            return self.getAnotherBrowser(url)
        self._drivers[0].get(self._config.testing_url + url)
        return self._drivers[0]

    def getAnotherBrowser(self, url=''):
        def close(driver):
            driver.close()
        mode = self._config.selenium_mode
        if mode == 'remote':
            driver = webdriver.Remote(self._config.selenium_url, self._config.desired_capabilities)
        elif mode == 'firefox':
            driver = webdriver.Firefox()
        elif mode == 'chrome':
            driver = webdriver.Chrome()
        else:
            raise NotImplementedError('Selenium mode is not supported yet: ' + mode)
        driver.get(self._config.testing_url + url)

        self._drivers.append(driver)
        self.addCleanup(close, driver)
        return driver

def avoidInBrowsers(*browserNames):
    config = BrowserConfiguration()
    config.loadDefaultFiles()
    message = 'The test has been skipped for browser: {}'
    return unittest.skipIf(config.browser_name in browserNames, message.format(browserNames))

def unlessInBrowsers(*browserNames):
    config = BrowserConfiguration()
    config.loadDefaultFiles()
    message = 'Current browser {} does not match any required browser for this test: {}'
    return unittest.skipIf(config.browser_name not in browserNames, message.format(config.browser_name, browserNames))
