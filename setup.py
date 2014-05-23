#!/usr/bin/env python
"""
Installation script:

To release a new version to PyPi:
- Change te version below
- Run: python setup.py sdist upload
"""

from setuptools import setup, find_packages

setup(name='django-oscar-unicredit',
      version="0.1.1",
      url='https://github.com/marcominutoli/django-oscar-unicredit',
      author="Marco Minutoli",
      author_email="info@marcominutoli.it",
      description="A plugin to pay with unicredit bank",
      long_description=open('README.rst').read(),
      keywords="E-commerce, Django, domain-driven, Payment, Unicredit",
      license='BSD',
      packages=find_packages(),
      install_requires=[],
      # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: Unix',
                   'Programming Language :: Python']
      )
