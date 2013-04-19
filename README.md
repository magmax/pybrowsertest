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
            page = self.browser.open('/')
            self.assertEquals("Directory listing for /", page.title)


This little code opens a browser, locates the page at '/' and checks
if the title is the given one.

Notice that the test class is inheriting from `BrowserTestCase`, and
how it has a public attribute in order to get a selenium driver
instance. It uses this driver to load a page and make the checks.


## Features ##

What makes this small framework so special?

- It is quite small.
- If one of your tests fails, **it will make a screenshot** from the last screen as additional data for debugging.
- It do not overwrite the methods `setUp` or `tearDown`, so it is safe for your current tests.
- It uses a new browser instance for each test. This is slow, but is the safer way to ensure you have a clean environment (no cookies, sessions or whatever).
- It reads the configuration from a file, what allows you to modify the file and run the tests again with another browser. You can change the configuration file or even set the configuration from your tests.
- It provides some useful decorators to avoid tests in some browsers.
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

Maybe you are not interested in using your own configuration file for one testing file. You can do that by setting the variable:

    from pybrowsertest import BrowserConfiguration
    BrowserConfiguration.default_configuration_files = ['whatever']

You can override every variable by hand in your tests:

    from pybrowsertest import BrowserConfiguration
    BrowserConfiguration.default_selenium_url = 'http://localhost:6666/wd/hub'
    BrowserConfiguration.default_selenium_mode = 'firefox'


## The API

Objects have been made as simple and expected as possible. So, you can access the browser directly from your tests by calling the attribute `browser`. Here you will find some methods very useful:

### browser

- `open(url)`: will load a new page. It will return a "page" object.
- `close()`: will finish the session and close the browser. Do not use it. It will be called automatically after each test.
- `refresh()`: will refresh current page.
- `back()`: go to the previous page in history, if possible.
- `forward()`: go to the next page in history, if possible.
- `add_cookie(key,value)`: add a cookie, with its _key_ and _value_.
- `get_cookie(key)`: retrieve a cookie by its _key_.
- `delete_cookie(key)`: remove a cookie, giving its _key_.
- `delete_all_cookies()`: clear all cookies.

### page

- `get_screenshot_as_file(filename)`: stores a PNG screenshot in the file _filename_.
- `find_element_by_css_selector(selector)`: retrieve the first element that matches the _selector_.
- `find_elements_by_css_selector(selector)`: retrieve all the elements that match the _selector_.
- `find_element_by_xpath(selector)`: retrieve the first element that matches the _selector_.
- `find_elements_by_xpath(selector)`: retrieve all the elements that match the _selector_.
- `find_element_by_tag_name(name)`: retrieve the first element with tag _name_.
- `find_elements_by_tag_name(name)`: retrieve all the elements with tag _name_.
- `find_element_by_class_name(name)`: retrieve the first element that has the class _name_.
- `find_elements_by_class_name(name)`: retrieve all the elements that has the class _name_.

To improve performance, all "find_*" methods will return a generator. And all of them have a optional parameter `timeout` that will wait some some time for the element to appear.


### widgets

There are a generic Widget type, but for some types, the most used attributes can be retrieved as the object attributes and the most used actions are objects methods.

All of them will have these methods, in addition to all the `find_*` ones:

- `click()`: simulate a mouse click on the widget.
- `get_attribute(name)`: retrieve the value of the attribute _name_.
- `is_displayed()`: True if the widget is shown.
- `is_enabled()`: True if the widget is enabled.

And the attributes:

- `id`: widget identifier
- `text`: text inside the widget
- `size`: A dict like: `{'width': 30, 'height': 30}` with the widget size.
- `location`: the location of the object.
- `tag_name`: the widget tag.


#### "A" Widget

The widget "a" will have some extra properties:

- `href`: target url
- `target`: url behavior.

#### "Input" Widget

The widget "input" will have some extra methods:

- `clear()`: removes any value
- `is_selected()`: True if the type is 'checkbox' or 'radio' and it is selected.
- `send_keys(keys)`: will type the keys one after another.

and properties:

- `type`: the type of input
- `value`: current value
- `placeholder`: text to show when no value.


#### "TextArea" Widget

The widget "textarea" will have some extra methods:

- `clear()`: removes any value
- `send_keys(keys)`: will type the keys one after another.

and properties:

- `rows`: number of rows
- `value`: current value
- `placeholder`: text to show when no value.

#### "Form" Widget

The widget "form" will have some extra methods:

- `submit()`: send the form.

and properties:

- `method`: POST or GET, usually.
- `action`: target url.



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

