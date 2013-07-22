#!/usr/bin/env python
# -*- mode:python; coding:utf-8; tab-width:4 -*-

import os
from setuptools import setup, Command

version = '0.0.2'

def read(fname):
    fullname = os.path.join(os.path.dirname(__file__), fname)
    with open(fullname) as f:
        return f.read()

setup(name         = 'pybrowsertest',
      version      = version,
      description  = 'Facility to use Selenium',
      long_description = read('README.md'),
      author       = 'Miguel Ángel García',
      author_email = '<miguelangel.garcia@tuenti.com>',
      license      = 'LGPL',
      url = "https://github.com/magmax/pybrowsertest",
      packages     = [
          'pybrowsertest',
          ],
      classifiers=[
          "Development Status :: 4 - Beta",
          "Topic :: Software Development :: Testing",
          "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
      ],
      install_requires=[req.strip()
                        for req in file('requirements.txt').readlines()
                        if req and req[0] not in '#-'],
      setup_requires=['nose>=1.0', 'nose-cov'],
      )
