# coding: utf-8
import os
from setuptools import setup
import coinbasev2.wallet

REQUIREMENTS = ["requests>=2.5", "six>=1.9", "pycryptodome>=3.4.11"]

setup(
    name='python-coinbasev2',
    version=coinbasev2.wallet.__version__,
    packages=['coinbasev2', 'coinbasev2.wallet'],
    include_package_data=True,
    description='Coinbase API client library',
    url='https://github.com/coinbase/coinbase-python/',
    download_url='https://github.com/coinbase/coinbase-python/tarball/%s' % (
        coinbasev2.wallet.__version__),
    keywords=['api', 'coinbase', 'bitcoin', 'oauth2', 'client'],
    install_requires=REQUIREMENTS,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
