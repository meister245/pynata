#!/usr/bin/env python3

import re
from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

with open('pynata/__init__.py', 'r') as f:
    version = re.search(r'(?<=__version__\s=\s\')(?:\d+\.\d+\.\d+)', f.read()).group(0)

project_urls = {
    'Changelog': 'https://github.com/meister245/pynata/wiki/Changelog',
    'Issue tracker': 'https://github.com/meister245/pynata/issues'
}

setup(
    name='pynata',
    version=version,
    url='https://github.com/meister245/pynata',
    license='MPL2.0',
    author='Zsolt Mester',
    author_email='contact@zsoltmester.com',
    description='python utility library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    project_urls=project_urls,
    packages=['pynata', 'pynata.logger'],
    python_requires='>=3.5.2',
    keywords='pynata utility logging',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
