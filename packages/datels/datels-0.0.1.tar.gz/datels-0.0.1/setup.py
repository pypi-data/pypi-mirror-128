from setuptools import setup, find_packages

LONG_DESCRIPTION = """
some long discription here.""".strip()

SHORT_DESCRIPTION ="""
some short discription here.""".strip()

VERSION = '0.0.1'
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)