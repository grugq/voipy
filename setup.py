#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup

name="voipy"
version="0.3.5"

setup(name=name,
        version=version,
        package_dir={'voipy' : 'voipy'},
        packages=['voipy', 'voipy.sip', 'voipy.events', 'voipy.mgcp', 'voipy.lib']
        )
