import unittest
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

def featuredAddFailure(original):
    def addFailure(self, test, err):
        test.save_screenshot()
        return original(test, err)
    return addFailure


class BrowserTestCase(unittest.TestCase):
    def __init__(self, *args, **kargs):
        unittest.TestCase.__init__(self, *args, **kargs)
        self._driver = None

    def run(self, result=None):
        if result is None:
            result = self.defaultTestResult()
        if result.addFailure != featuredAddFailure:
            func_type = type(result.addFailure)
            result.addFailure = func_type(featuredAddFailure(result.addFailure), result, unittest.TestResult)

        return unittest.TestCase.run(self, result)

    def save_screenshot(self):
        if self._driver is not None:
            self._driver.save_screenshot('error.{0}.{1}.png'.format(self.id(), time.time()))

    def getBrowser(self, url=''):
        def close(driver):
            driver.close()
        if self._driver is None:
            self._driver = webdriver.Remote('http://localhost:4444/wd/hub', {'browserName': 'firefox'})
            self.addCleanup(close, self._driver)

        self._driver.get('http://localhost:8000/' + url)
        return self._driver


