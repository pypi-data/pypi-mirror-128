#!/usr/bin/env python
import os
from setuptools import setup, find_packages

with open('README.md', encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='nautobot-move',
    author='Gesellschaft für wissenschaftliche Datenverarbeitung mbH Göttingen',
    version='0.1.0',
    license='Apache-2.0',
    url='https://gitlab.gwdg.de/gwdg-netz/nautobot-plugins/nautbot-move',
    description='A Nautobot plugin for moving devices',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages('.'),
    include_package_data=True,
    install_requires=[],
    zip_safe=False,
)

