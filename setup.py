#!/usr/bin/env python3

import re
from setuptools import setup, find_namespace_packages

with open('README.md', 'r') as f:
    long_description = f.read()

with open('pynata/__init__.py', 'r') as f:
    version = re.search(r'(?<=__version__\s=\s\')(?:\d+\.\d+\.\d+)', f.read()).group(0)

extras_require = {
    'web': ['requests']
}

project_urls = {
    'Changelog': 'https://gitlab.com/meister245/pynata/wikis/Changelog',
    'Issue tracker': 'https://gitlab.com/meister245/pynata/issues'
}

setup(
    name='pynata',
    version=version,
    url='https://gitlab.com/meister245/pynata',
    license='MPL2.0',
    author='Zsolt Mester',
    author_email='contact@zsoltmester.com',
    maintainer='Project Service Desk',
    maintainer_email='incoming+meister245/pynata@incoming.gitlab.com',
    description='Python utility library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    project_urls=project_urls,
    packages=['pynata', 'pynata.template', 'pynata.util'],
    python_requires='>=3.5.2',
    keywords='pynata utility logging',
    extras_require=extras_require,
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
