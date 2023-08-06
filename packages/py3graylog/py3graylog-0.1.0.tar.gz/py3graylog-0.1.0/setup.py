#!/usr/bin/env python
# coding：<encoding name> ： # coding: utf-8

from distutils.core import setup

setup(name='py3graylog',
      version='0.1.0',
      description='基于Zack Allen老师的pygraylog，升级成为支持Python3的执行调用。',
      author='糖果',
      author_email='49263457@qq.com',
      url='https://www.github.com/shengnoah/py3graylog',
      download_url='https://github.com/shengnoah/py3graylog/tarball/0.1.0',
      packages=['py3graylog'],
      keywords=['graylog', 'graylog-api', 'api graylog'],
      install_requires=[
          'requests'
      ],
     )
