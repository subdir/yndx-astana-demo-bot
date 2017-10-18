#!/usr/bin/env python

from distutils.core import setup

setup(
    name='yndx_astana_demo_bot',
    version = '0.1',
    url = 'https://github.com/subdir/yndx-astana-demo-bot',
    packages = ['yndx_astana_demo_bot'],
    install_requires = [
        'python-telegram-bot',
        'requests',
        'numpy',
        'scipy',
        'sklearn',
        'python_speech_features',
        'seaborn',
        'matplotlib'
    ],
    scripts = [
        'bot.py'
    ]
)

