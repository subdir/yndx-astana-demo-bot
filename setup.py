#!/usr/bin/env python

from distutils.core import setup

setup(
    name='yndx_astana_demo_bot',
    version = '0.1',
    url = 'https://github.com/subdir/yndx-astana-demo-bot',
    packages = ['yndx_astana_demo_bot'],
    requires = [
        'matplotlib',
        'numpy',
        'python_speech_features',
        'python_telegram_bot',
        'requests',
        'scipy',
        'seaborn',
        'sklearn',
    ],
    scripts = [
        'bot.py'
    ]
)

