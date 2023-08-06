# -*- coding: utf-8-*-
from setuptools import setup, find_packages
setup(
    # 以下为必需参数
    name='scrapyer-rabbitmq-scheduler',  # 模块名
    version='1.0.8',  # 当前版本
    description='Rabbitmq for Distributed scraping',  # 简短描述
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
