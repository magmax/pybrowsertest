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

## Configuration ##

PyBrowserTest is highly configurable. You can use three files to
configure it. From the lowest priority to the highest:

- `/etc/pybrowsertest.cfg`
- `.pybrowsertest.cfg`
- `pybrowsertest.cfg`

Files will have the tipical INI files format, with sections and keywords.
Lets study them:

### Section global ###

Example:

    [global]
    selenium_url = http://localhost:4444/wd/hub
    testing_url = http://localhost
    screenshot_file_pattern = error.{testname}.{timestamp}.png

#### selenium_url ####

**Default**: http://localhost:4444/wd/hub

Url where selenium server is listening

#### testing_url ####

**Default**: http://localhost

Url base to start tests. All requests will be made from with this url as base url.

#### screenshot_file_pattern ####

**Default**: error.{testname}.{timestamp}.png

Pattern to store the screenshots. You can use some variables here, surrounded with brackets*****. The default value is an example. You can use the next values:

- **testname**: Name of the current test
- **timestamp**: seconds from Epoch. Decimals are the milliseconds.

### Section desired capabilities ###

Example:

    [desired capabilities]
    browserName = firefox
    javascriptEnabled = True

Here you can add whatever capabilities you desire. If they are
available in the driver you choose, they will be used.

There are some common capabilities, like "**browserName**" and
"**javascriptEnabled**". Check the Selenium documentation to see all
of them.
