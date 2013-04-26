#!/usr/bin/python
# -*- mode:python; coding:utf-8; tab-width:4 -*-

import sys
import traceback
import unittest
from string import Template

CONFIG_TEMPLATE="""
[global]
testing_url = http://localhost:8000
screenshot_file_pattern = error.{testname}.{timestamp}.png
selenium_mode = ${selenium_mode}
selenium_url = http://localhost:4444/wd/hub

[desired capabilities]
browserName = ${browser}
javascriptEnabled = True
"""

class TestResultWrapper(unittest.TestResult):
    def __init__(self, *args, **kargs):
        unittest.TestResult.__init__(self, *args, **kargs)
        self._current_browser = None
        self._total = 0

    def setBrowser(self, browser):
        self._current_browser = browser

    def parseSkipped(self):
        pass

    def addError(self, test, err):
        print 'ERROR:'
        print test
        traceback.print_tb(err[2])
        print err[1]
        unittest.TestResult.addError(self, test, err)

    def addFailure(self, test, err):
        if 'fail' == self._getExpectedResult(test):
            self._success(test)
        else:
            self._failure(test, err)

    def addSuccess(self, test):
        self._success(test)

    def addSkip(self, test, reason):
        expected = self._getExpectedResult(test)
        if 'skip' == expected:
            self._success(test)
        elif 'skipif' == expected and self._current_browser in reason.split(':')[1]:
            self._success(test)
        elif 'skipifnot' == expected and self._current_browser not in reason.split(':')[1]:
            self._success(test)
        else:
            self._failure(test, (None, reason, None))

    def addExpectedFailure(self, test, err):
        self._failure(test, (None, None, None))

    def addUnexpectedSuccess(self, test):
        self._failure(test, (None, None, None))

    def _success(self, test):
        self._total += 1
        unittest.TestResult.addSuccess(self, test)
        sys.stdout.write('.')
        sys.stdout.flush()

    def _failure(self, test, err):
        unittest.TestResult.addFailure(self, test, err)
        sys.stdout.write('F')
        sys.stdout.flush()

    def _getExpectedResult(self, test):
        data = test.id().split('_', 3)
        if len(data) < 3:
            return None
        return data[1]

    def __str__(self):
        result = ''

        for fail in self.failures:
            result += '{} -> {}\n'.format(fail[0].id(), fail[1])

        result += '\n'
        if self.errors:
            result += 'ERRORS: '
        elif self.failures:
            result += 'FAILED: '
        else:
            result += 'SUCCESS: '
        msg = ['{} tests executed'.format(self._total)]
        if self.skipped:
            msg.append('{} tests skipped'.format(len(self.skipped)))
        if self.failures:
            msg.append('{} tests failed'.format(len(self.failures)))
        if self.errors:
            msg.append('{} tests erroneous'.format(len(self.errors)))
        result += ', '.join(msg)
        return result


class Runner():
    def __init__(self):
        self._template = Template(CONFIG_TEMPLATE)

    def run(self, mode, browser):
        self.writeConfigFile(mode, browser)

        result = TestResultWrapper()
        result.setBrowser(browser)

        loader = unittest.TestLoader()
        for suite in loader.discover('test', pattern='test*.py'):
             suite.run(result)

        print
        print result
        sys.exit(0 if result.wasSuccessful() else 2)

    def writeConfigFile(self, mode, browser):
        with file('browsertest.cfg', 'w+') as fd:
            fd.write(self._template.safe_substitute(browser=browser, selenium_mode=mode))
            fd.flush()


if __name__ == '__main__':
    mode = sys.argv[1]
    browser = sys.argv[2] if mode == 'remote' else mode
    runner = Runner()
    runner.run(mode, browser)
