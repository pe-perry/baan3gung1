# -*- coding: utf-8 -*-

from setuptools import setup


def readme():
    with open('README.md', 'rb') as f:
        return f.read().decode()


setup(
    name='baan3gung1',
    version='0.1.5',
    description='Get bored? Take a break!',
    long_description='Get bored? Take a break!',
    keywords='baan3gung1 hea work',
    url='https://github.com/kitman0804/baan3gung1',
    author='kitman0804 @ https://github.com/kitman0804',
    author_email='kitman0804@gmail.com',
    license='MIT',
    packages=[
        'baan3gung1',
        'baan3gung1.lihkg',
    ],
    install_requires=[
        'requests',
        'lxml',
        'beautifulsoup4',
    ],
    include_package_data=True,
    zip_safe=False
)

