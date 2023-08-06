#!/usr/bin/env python

from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as file:
    long_description = file.read()

with open("requirements.txt", encoding="utf-8") as file:
    install_requires = list(val.strip() for val in file.readlines())

setup(
    name="load-shedding",
    version="0.2.1",
    author="Werner Pieterson",
    description="A python library for getting Load Shedding schedules from Eskom.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://gitlab.com/wernerhp/load-shedding",
    license="GPLv3+",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.8",
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.9",
    ],
)