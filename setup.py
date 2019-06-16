# coding: utf-8
from __future__ import unicode_literals

from setuptools import setup, find_packages


setup(
    name='razdel',
    version='0.4.0',
    description='Splits russian text into tokens, sentences, section. Rule-based',
    url='https://github.com/natasha/razdel',
    author='Alexander Kukushkin',
    author_email='alex@alexkuk.ru',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='natural language processing, russian, token, sentence',
    packages=find_packages(),
)
