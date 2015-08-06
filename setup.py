#!/usr/bin/python

from setuptools import setup

setup(name='appoints',
        version='1.1a2',
        description='A Library for managing appointments',
        author='Philip Wellnitz',
        author_email='philipwellnitz@gmx.de',
        url='https://github.com/PH111P/appoints',
        packages=['appoints'],
        extras_require={
            'Twofish encryption': ['twofish']
        }
    )
