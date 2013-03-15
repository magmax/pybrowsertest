import os
import unittest
import time
from ConfigParser import ConfigParser
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

__all__ = ['BrowserTestCase']


def featuredAddFailure(original):
    def addFailure(self, test, err):
        test.save_screenshot()
        return original(test, err)
    return addFailure


class BrowserConfiguration(object):
    SECTION_GLOBAL = 'global'
    SECTION_DESIRED = 'desired capabilities'

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
        self._config.set(self.SECTION_GLOBAL, self.OPTION_TESTING_URL, 'http://localhost')
        self._config.set(self.SECTION_GLOBAL, self.OPTION_SCREENSHOT_PATTERN, 'error.{testname}.{timestamp}.png')

        self._config.add_section(self.SECTION_DESIRED)
        self._config.set(self.SECTION_DESIRED, self.OPTION_BROWSER_NAME, 'firefox')
        self._config.set(self.SECTION_DESIRED, self.OPTION_JAVASCRIPT, 'true')

    def load(self, filelist):
        for filename in filelist:
            if os.path.exists(filename):
                self._config.read(filename)

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
    def desired_capabilities(self):
        desired = {}
        for option in self._config.options(self.SECTION_DESIRED):
            desired[option] = self._config.get(self.SECTION_DESIRED, option)
        print desired
        return desired


class BrowserTestCase(unittest.TestCase):
    def __init__(self, *args, **kargs):
        unittest.TestCase.__init__(self, *args, **kargs)

        self._drivers = []
        self._config = BrowserConfiguration()
        self._config.load(['/etc/browsertests.cfg', '.browsertests.cfg', 'browsertests.cfg'])

    def run(self, result=None):
        if result is None:
            result = self.defaultTestResult()
        if result.addFailure != featuredAddFailure:
            func_type = type(result.addFailure)
            result.addFailure = func_type(featuredAddFailure(result.addFailure), result, unittest.TestResult)

        return unittest.TestCase.run(self, result)

    def save_screenshot(self):
        if len(self._drivers) != 0:
            filename = self._config.screenshot_file_pattern.format(testname=self.id(), timestamp=time.time())
            self._drivers[0].save_screenshot(filename)

    def getBrowser(self, url=''):
        if len(self._drivers) == 0:
            return self.getAnotherBrowser(url)
        self._drivers[0].get(self._config.testing_url + url)
        return self._drivers[0]

    def getAnotherBrowser(self, url=''):
        def close(driver):
            driver.close()
        driver = webdriver.Remote(self._config.selenium_url, self._config.desired_capabilities)
        driver.get(self._config.testing_url + url)

        self._drivers.append(driver)
        self.addCleanup(close, driver)
        return driver

