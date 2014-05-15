#!/usr/bin/env python
# -*- mode:python; coding:utf-8; tab-width:4 -*-

import os
from setuptools import setup, Command
from pybrowsertest import __version__


def read(filename):
    with open(filename) as fd:
        return fd.read()

setup(name         = 'pybrowsertest',
      version      = __version__,
      description  = 'Facility to use Selenium',
      long_description = read('README.rst'),
      author       = 'Miguel Ángel García',
      author_email = '<miguelangel.garcia@tuenti.com>',
      license      = 'LGPL',
      url          = "https://github.com/magmax/pybrowsertest",
      packages     = [
          'pybrowsertest',
          ],
      package_data = {
        '': ['*.txt', '*.rst'],
      },
      classifiers=[
          "Development Status :: 4 - Beta",
          "Topic :: Software Development :: Testing",
          "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: User Interfaces',
          'Topic :: Software Development :: Libraries :: Application Frameworks',
      ],
      install_requires=[
          'selenium==2.41.0',
      ],
)
