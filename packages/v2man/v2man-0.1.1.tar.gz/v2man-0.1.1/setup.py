#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="v2man",
    version="0.1.1",
    license="MIT Licence",
    description="A v2ray python client based on v2ray gRPC API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Unixeno",
    author_email="li139793780@gmail.com",
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        "grpcio==1.42.0",
        "grpcio-tools==1.42.0"
    ],
    entry_points={
        'console_scripts': [
            'v2man-gen=v2man.gen:main',
        ],
    },
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
