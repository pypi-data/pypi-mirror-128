# -*- coding:utf-8 -*-
# ========================================
# Author: Chris Huang
# Mail: 
# Data: 2021/6/24
# ========================================
from __future__ import print_function
from setuptools import setup, find_packages
VERSION = '1.8'


setup(
    name="tkfab",
    version=VERSION,
    author="TimHuang",
    author_email="1400471035@qq.com",
    description="fast user fabric3",
    long_description=open("README.md").read(),
    license="Apache License",
    url="",
    packages=find_packages(),
    # data_files=[
    #     ('', 'allure_pytest_listener.txt'),
    # ],
    package_data={
        '': ['*.txt']
    },
    install_requires=[
        'fabric3',
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        'Programming Language :: Python :: 3.7',
    ],
)