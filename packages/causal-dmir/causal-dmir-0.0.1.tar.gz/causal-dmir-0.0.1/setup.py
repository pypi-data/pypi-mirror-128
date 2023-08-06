# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import causaldmir

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

VERSION = causaldmir.__version__

setup(
    name="causal-dmir",
    version=VERSION,
    description="Causal-dmir Library: Causal Discovery Modeling, Identification and Reasoning",
    license="GPL",
    author="DMIRLab",
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
    ]
)
