# -*- coding: utf-8 -*-

from os import listdir
from os.path import isfile, join
from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

def get_email_dependencies():    
    path = join('dividend-analyzer', 'email')
    file_list = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
    return file_list

setup(
    name='dividend-analyzer',
    version='0.0.1',
    description='App for fetching and analyzing dividend data for a list of stock tickers.',
    long_description=readme,
    author='Paris Ambush',
    author_email='paris.ambush@gmail.com',
    url='https://github.com/pambushdev-test-org/dividend-analyzer',
    license=license,
    data_files=[('email', get_email_dependencies())],
    packages=find_packages(exclude=('tests', 'docs'))
)