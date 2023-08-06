# -*- coding: utf-8-*-
from setuptools import setup, find_packages
import os,io

here = os.path.abspath(os.path.dirname(__file__))
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


setup(
    # 以下为必需参数
    name='scrapyer-rabbitmq-scheduler',  # 模块名
    version='1.0.9',  # 当前版本
    description='Rabbitmq for Distributed scraping',  # 简短描述
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='buliqioqiolibusdo',
    author_email='dingyeran@163.com',
    license='MIT',
    url='https://github.com/aox-lei/scrapy-rabbitmq-scheduler',
    install_requires=[
        'pika',
    ],
    packages=['scrapy_rabbitmq_scheduler'],
    package_dir={'': 'src'}
)
