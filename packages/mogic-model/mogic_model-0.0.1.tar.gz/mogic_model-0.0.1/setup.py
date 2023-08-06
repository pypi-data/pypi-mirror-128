#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: gm
# Mail: 1025304567@qq.com
# Created Time: 2019-04-11 15:37:04
#############################################


from setuptools import setup, find_packages

setup(
    name = "mogic_model",
    version = "0.0.1",
    keywords = ("pip", "license","licensetool", "tool", "gm"),
    description = "mogic_model",
    long_description = "mogic_model",
    license = "MIT Licence",

    url = "https://gitlab.com/ancientchaos/licensetool",
    author = "gm",
    author_email = "1025304567@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['chardet']
)
