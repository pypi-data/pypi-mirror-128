#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='pyrof',
    packages=find_packages(),
    version='0.1.0',
    description='Python wrappers for dynamic menus (rofi, fzf)',
    url='https://github.com/nesstero/pyrof',
    license='MIT',
    maintainer='nesstero',
    maintainer_email='nestero@tuta.io',
    install_requires=['traitlets']
)
