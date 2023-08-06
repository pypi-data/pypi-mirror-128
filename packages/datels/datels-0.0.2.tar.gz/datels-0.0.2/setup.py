from setuptools import setup

LONG_DESCRIPTION = """
`datels` is a simple CLI that displays a list of dates line by line.""".strip()

SHORT_DESCRIPTION ="""
`datels` is a simple CLI that displays a list of dates line by line.""".strip()

VERSION = '0.0.2'
URL = 'https://github.com/joe-yama/datels'

DEPENDENCIES = []
TEST_DEPENDENCIES = []
with open('requirements.txt') as requirements_txt:
    DEPENDENCIES = requirements_txt.read().splitlines()

setup(
    name='datels',
    version=VERSION,
    description=SHORT_DESCRIPTION,
    author='joe-yama',
    
    packages=['datels'],
    install_requires=DEPENDENCIES,
    entry_points={
        "console_scripts": [
            "datels=datels.core:main",
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)