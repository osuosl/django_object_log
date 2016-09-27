#!/usr/bin/env python

from setuptools import setup

long_desc = open('README.rst').read()

setup(name='django-object-log',
      version="0.7.1",
      description='A method for logging user actions on models',
      long_description=long_desc,
      author='Peter Krenesky',
      author_email='peter@osuosl.org',
      maintainer="Corbin Simpson",
      maintainer_email="simpsoco@osuosl.org",
      url='http://code.osuosl.org/projects/django-object-log',
      packages=['object_log'],
      include_package_data=True,
      zip_safe=False,
      classifiers=[
          "License :: OSI Approved :: MIT License",
          'Framework :: Django',
          ],

      # Enable django-setuptest
      test_suite='setuptest.setuptest.SetupTestSuite',
      tests_require=(
        'django-setuptest',
        # Required by django-setuptools on Python 2.6
        'argparse'
      ),
      )
