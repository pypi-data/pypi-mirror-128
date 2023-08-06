#!/usr/bin/env python
"""The setup script."""
import ionized

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['amazon.ion']

test_requirements = ['pytest>=3', ]

setup(
    author="Theo \"Bob\" Massard",
    author_email='tbobm@protonmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Bootstrap Amazon Ion into existing projects",
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='ionized',
    name='ionized',
    packages=find_packages(include=['ionized', 'ionized.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/tbobm/ionized',
    version=ionized.__version__,
    zip_safe=False,
)
