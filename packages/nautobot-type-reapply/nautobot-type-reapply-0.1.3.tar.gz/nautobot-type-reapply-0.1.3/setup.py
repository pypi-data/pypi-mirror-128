#!/usr/bin/env python
import os
from setuptools import setup, find_packages

with open('README.md', encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='nautobot-type-reapply',
    author='Gesellschaft für wissenschaftliche Datenverarbeitung mbH Göttingen',
    author_email = "netzadmin@gwdg.de",
    version='0.1.3',
    license='Apache-2.0',
    url='https://gitlab.gwdg.de/gwdg-netz/nautobot-plugins/nautobot-type-reapply',
    description='A Nautobot plugin for re-appling device types',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages('.'),
    include_package_data=True,
    install_requires=[],
    zip_safe=False,
)

