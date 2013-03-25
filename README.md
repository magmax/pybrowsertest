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
- You can use your favourite runner: [unittest.main](http://docs.python.org/2/library/unittest.html#basic-example), [nosetests](https://nose.readthedocs.org/en/latest/), [zope.testrunner](https://pypi.python.org/pypi/zope.testrunner), [pytong](https://code.google.com/p/pytong/),... or even your own runner ([just like I had to do to test it](https://github.com/magmax/pybrowsertest/blob/master/run_tests.py))

## Decorators ##

Not all the browsers work in the same way, so there will be some tests
that cannot be executed in some of them. Because of that, this
framework provides some decorators to make the developer's life
easier:

### onlyIfBrowserIn ###

This decorator will allow you to exclude the test only for some browsers.

Example:

    @onlyIfBrowserIn('chrome', 'firefox')
    def test_example(self):
        pass

### onlyIfBrowserNotIn ###

The opposite to `onlyIfBrowserIn`, only will execute the test if you
are using these browsers.

    @onlyIfBrowserNotIn('chrome', 'firefox')
    def test_example(self):
        pass


## Configuration ##

PyBrowserTest is highly configurable. You can use three files to
configure it. From the lowest priority to the highest:

- `/etc/pybrowsertest.cfg`
- `.pybrowsertest.cfg`
- `pybrowsertest.cfg`

Files will have the tipical INI files format, with sections and keywords.

Please, check the file [browsertest.cfg.template](https://github.com/magmax/pybrowsertest/blob/master/browsertest.cfg.template) for more information.


## Contributing ##

If you want to contribute, you should know how to run the tests. These are the steps after cloning the repository:

    # You will need a Server running. You can use your own... or this:
    make tests_server

    # This command will download all what you need for you:
    make tests

Be careful: That command will let you to stop the selenium server and the local server.

If you want to see a cleaner window, just start the selenium server and the local server in different windows or redirect its output to `/dev/null`.


### Our own runner ###

In order to test this framework, it has been necessary to build our own runner. It was necessary to catch the skipped tests, to check if they were really skipped; to catch the failed tests, to check if they were really failing, and so on. So you need to run the `./run_tests.py` script in order to test the own pybrowsertest library.

Remember: the `./run_tests.py` script is not useful for your own tests; only in this library.

