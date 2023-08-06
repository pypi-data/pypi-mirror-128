#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
import re
import os

NAME = 'SpiderKo'

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

re_meta = re.compile(r'__(\w+?)__\s*=\s*(.*)')
re_doc = re.compile(r'^"""(.+?)"""')


def _add_default(m):
    attr_name, attr_value = m.groups()
    return ((attr_name, attr_value.strip("\"'")),)


def _add_doc(m):
    return (('doc', m.groups()[0]),)


def parse_dist_meta():
    """Extract metadata information from ``$dist/__init__.py``."""
    pats = {re_meta: _add_default, re_doc: _add_doc}
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, NAME, '__init__.py')) as meta_fh:
        distmeta = {}
        for line in meta_fh:
            if line.strip() == '# -eof meta-':
                break
            for pattern, handler in pats.items():
                m = pattern.match(line.strip())
                if m:
                    distmeta.update(handler(m))
        return distmeta


meta = parse_dist_meta()
requires = [
    'requests',
    'xlrd==1.2.0',
    'pandas',
    'BeautifulSoup4',
    'simplepy',
    'redis',
    'pymongo'
]
setup(
    name=NAME,
    version=meta['version'],
    author=meta['author'],
    author_email=meta['contact'],
    url=meta['url'],
    description='Spider Toolkit Collection',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'spider = SpiderKo.__main__:main'
        ]
    }
)
