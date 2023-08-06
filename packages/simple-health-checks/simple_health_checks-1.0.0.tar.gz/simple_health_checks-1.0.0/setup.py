import os

from setuptools import setup

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(dir_path, "./VERSION"), "r", encoding="utf-8") as version_file:
    version = str(version_file.readline()).strip()

setup(version=version)
