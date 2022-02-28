#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    name='django-permissionedforms',
    version='0.1',
    description="Django extension for creating forms that vary according to user permissions",
    author='Matthew Westcott',
    author_email='matthew.westcott@torchbox.com',
    url='https://github.com/wagtail/django-permissionedforms',
    packages=find_packages(exclude=('tests*',)),
    license='BSD',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    install_requires=[
        'Django',
    ],
    extras_require={
        'testing': [
            'django-modelcluster',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
        'Framework :: Django',
    ],
)
