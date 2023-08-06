import os
from pathlib import Path

from setuptools import setup

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(dir_path, "./VERSION"), "r", encoding="utf-8") as version_file:
    version = str(version_file.readline()).strip()

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    version=version,
    long_description=long_description,
    long_description_content_type="text/markdown",
)
