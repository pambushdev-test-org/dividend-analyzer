# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='dividend-analyzer',
    version='0.0.1',
    description='App for fetching and analyzing dividend data for a list of stock tickers.',
    long_description=readme,
    author='Paris Ambush',
    author_email='paris.ambush@gmail.com',
    url='https://github.com/pambushdev-test-org/dividend-analyzer',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

