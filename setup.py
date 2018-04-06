
from setuptools import setup

setup(
    name = 'xibbaz',
    version = '0.1.0',
    author = 'Erik Stephens',
    author_email = 'erik@tfks.net',
    description = 'A Pythonic interface to the Zabbix API',
    license = 'MIT',
    keywords = 'zabbix api',
    url = 'http://github.com/erik-stephens/xibbaz',
    packages = ['xibbaz', 'xibbaz.objects', 'tests'],
    long_description = open('README.rst').read(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
)
