#!/usr/bin/env python
"""
ProjectManager
==============
The Project Manager provides support for managing application based on Python

"""
import os
import sys

from setuptools import setup

install_requires = []
if sys.version_info < (2, 7):
    install_requires += ['argparse']

readme_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'README.md')

setup(
    name='pypm',
    version='0.0.1',
    url='https://github.com/myevan/pypm',
    license='MIT',
    author='myevan',
    author_email='myevan@outlook.com',
    description='Project Manager base on Python',
    long_description=open(readme_path).read(),
    packages=[
        'pypm'
    ],
    zip_safe=False,
    install_requires=install_requires,
    tests_require=[
        'pytest',
    ],
    platforms='any',
)
