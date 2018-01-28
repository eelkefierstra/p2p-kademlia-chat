#!/usr/bin/env python3
from setuptools import setup, find_packages
import unittest

# Needed to locate the p2pchat package
import sys
sys.path.append('src/')

with open("requirements.txt") as reqfile:
    required = reqfile.read().splitlines()

def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('src/test/', pattern='test_*.py')
    return test_suite

setup(
        name="p2pchat-client",
        description="The client for p2pchat",
        url="https://github.com/eelkefierstra/p2p-kademlia-chat",
        license="MIT",
        packages=find_packages(),
        install_requires=required,
        test_suite='setup.my_test_suite'
)

