# -*- coding: utf-8 -*-
import os
from setuptools import setup
from setuptools import find_packages

version = '1.8'

install_requires = ['croniter', 'tzlocal']
test_requires = ['coverage']


def read(name):
    with open(os.path.join(os.path.dirname(__file__), name)) as f:
        return f.read()


setup(
    name='aiocron',
    version=version,
    description="Crontabs for asyncio",
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='crontab cron asyncio',
    author='Gael Pasgrimaud',
    author_email='gael@gawel.org',
    url='https://github.com/gawel/aiocron/',
    license='MIT',
    packages=find_packages(exclude=['docs', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'test': test_requires,
    },
)
