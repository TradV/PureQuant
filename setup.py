# -*- coding:utf-8 -*-

from distutils.core import setup


setup(
    name="purequant",
    version="0.0.1",
    packages=[
        "purequant",
        "purequant.example",
        "purequant.example.double_moving_average_strategy",
        "purequant.utils",
        "purequant.exchange.okex",
        "purequant.exchange.huobi",
    ],
    include_package_data = True,
    platforms = "any",
    description="Professional quantitative trading framework.",
    url="https://github.com/eternalranger/PureQuant",
    author="eternal ranger",
    author_email="interstella.ranger2020@gmail.com",
    license="MIT",
    keywords=[
        "purequant", "quant", "framework", "okex", "trade", "btc"
    ],
    install_requires=[
        'numpy',
        'requests',
        'urllib3',
        'chardet',
        'certifi',
        'idna',
        'twilio',
        'six',
        'mysql',
        'mysql-connector-python'
    ],
)
