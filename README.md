# PyBrowserTest#

PyBrowserTest is a (very) small framework used to create Browser tests.

It wraps all the selenium initializations in order to make easier to
begin with these kind of tests. It is very flexible and can be used
with your favourite runner.

PyBrowserTest opens a clean environment for each test. It is slow, but
safe.

It requires python-selenium to work properly, since it is only a
wrapper for it.

## An example ##

Lets start with a full example:

    import unittest
    from pybrowsertest import BrowserTestCase

    class AutomationTest(BrowserTestCase):
        def test_the_title_is_set(self):
            browser = self.getBrowser()
            self.assertEquals("Directory listing for /", browser.title)


This little code opens a browser and checks if the title is the given
one.

Notice that the test class is inheriting from `BrowserTestCase`, and how it calls to `getBrowser` in order to get a selenium driver instance.


## Features ##

What makes this small framework so special?

- It is quite small.
- If one of your tests fails, it will make a screenshot from the last screen as additional data for debugging.
- It do not overwrite the methods `setUp` or `tearDown`, so it is safe for your current tests.
- It uses a new browser instance for each test. This is slow, but is the safer way to ensure you have a clean environment (no cookies, sessions or whatever).
- It reads the configuration from a file, what allows you to modify the file and run the tests again with another browser.
- It provides some useful decorators to avoid tests in some browsers


## Decorators ##

Not all the browsers work in the same way, so there will be some tests
that cannot be executed in some of them. Because of that, this
framework provides some decorators to make the developer's life
easier:

### avoidInBrowsers ###

This decorator will allow you to exclude the test only for some browsers.

Example:

    @avoidInBrowsers('chrome', 'firefox')
    def test_example(self):
        pass

### unlessInBrowsers ###

The opposite to `avoidInBrowsers`, only will execute the test if you
are using these browsers.

    @unlessInBrowsers('chrome', 'firefox')
    def test_example(self):
        pass


## Configuration ##

PyBrowserTest is highly configurable. You can use three files to
configure it. From the lowest priority to the highest:

- `/etc/pybrowsertest.cfg`
- `.pybrowsertest.cfg`
- `pybrowsertest.cfg`

Files will have the tipical INI files format, with sections and keywords.

Please, check the file browsertest.cfg.template for more information.
