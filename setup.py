from setuptools import setup, find_packages
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='circum-hc-sr04',
    version_format='{tag}',
    author="Lane Haury",
    author_email="lane@lumineerlabs.com",
    description="HC-SR04 sensor plugin for circum.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/LumineerLabs/circum-hc-sr04",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        'circum',
        'click',
        'gpiod',
        'RPi.GPIO2',
    ],
    setup_requires=[
        'setuptools',
        'setuptools-git-version',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
    ],
    entry_points={
        'console_scripts': [
            'calibrate-hc-sr04=circum_hc_sr04.calibrate:cli',
        ],
        'circum.sensors': [
            'hc-sr04=circum_hc_sr04.hc_sr04:hc_sr04_command'
        ]
    },
    extras_require={
        'lint': [
            'flake8',
            'flake8-import-order',
            'flake8-builtins',
            'flake8-comprehensions',
            'flake8-bandit',
            'flake8-bugbear',
        ]
    },
    python_requires=">=3.7",
)
