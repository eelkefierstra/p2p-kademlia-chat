#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("requirements.txt") as reqfile:
    required = reqfile.read().splitlines()

setup(
        name="p2pchat-client",
        description="The client for p2pchat",
        url="https://github.com/eelkefierstra/p2p-kademlia-chat",
        license="MIT",
        packages=find_packages(),
        install_requires=required
)

