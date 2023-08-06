# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.md", encoding='utf-8').read()
except IOError:
    long_description = ""

setup(
    name="qrunner",
    version="0.4.5",
    description="UI自动化测试框架",
    author="杨康",
    author_email="772840356@qq.com",
    url="https://github.com/bluepang/qrunner",
    platforms="Android,IOS",
    packages=find_packages(),
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
    ],
    include_package_data=True,
    package_data={
        r'': ['*.exe'],
    },
    install_requires=['tidevice', 'facebook-wda', 'uiautomator2', 'selenium', 'pytest', 'pytest-html',
                      'pytest-rerunfailures', 'allure-pytest', 'pytest-dependency==0.5.1'],
    entry_points={
        'console_scripts': [
            'qrun = qrunner.cli:main'
        ]
    },
)
