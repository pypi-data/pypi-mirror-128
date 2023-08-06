#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = []

test_requirements = [
    "pytest==6.2.5",
    "pytest-mock==3.6.1",
]

setup(
    author="Alex Macniven",
    author_email="alex_macniven@icloud.com",
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    description=(
        "Postman-Py provides a thin wrappers around the built-in package for sending"
        " mail."
    ),
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="postman_py",
    name="postman_py",
    packages=find_packages(include=["postman_py", "postman_py.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/alexmacniven/postman_py",
    version="0.1.0",
    zip_safe=False,
)
