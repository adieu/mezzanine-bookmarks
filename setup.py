#!/usr/bin/env python
from setuptools import setup, find_packages


with open('README.rst') as file:
    long_description = file.read()


setup(
    name = "mezzanine-bookmarks",
    version = "0.1",
    license = 'BSD',
    description = "Bookmark Service built on Django and Mezzanine.",
    long_description=long_description,
    author='Ivan Diao',
    author_email='adieu@adieu.me',
    url='http://github.com/adieu/mezzanine-bookmarks',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    entry_points={
        'console_scripts': [
            'bookmarks = bookmarks.utils.runner:main',
        ],
    },
    install_requires = (
        'mezzanine',
        'logan',
        'Django'
    ),
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
)
