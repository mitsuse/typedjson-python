#!/usr/bin/env python3
# coding: utf-8

from setuptools import find_packages
from setuptools import setup


def _read(path: str) -> str:
    with open(path) as fp:
        return fp.read()


setup(
    name='typedjson',
    version='0.7.1',
    description='JSON decoding for Python with type hinting (PEP 484)',
    long_description=_read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/mitsuse/typedjson-python',
    author='Tomoya Kose',
    author_email='tomoya@mitsuse.jp',
    install_requires=[
        'dataclasses>=0.6.0,<1.0.0;python_version<"3.7"',
        'typing-extensions>=3.6.6,<4.0.0',
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords=[],
    packages=find_packages(exclude=[
        'tests',
        'fixtures',
    ]),
    entry_points={
        'console_scripts': [],
    },
)
