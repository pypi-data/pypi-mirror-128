from setuptools import setup

SHORT_DESCRIPTION = """
`datels` is a simple CLI that displays a list of dates line by line.""".strip()
with open('README.md') as readme:
    LONG_DESCRIPTION =readme.read().strip()

VERSION = '0.1.3'
URL = 'https://github.com/joe-yama/datels'

DEPENDENCIES = []
TEST_DEPENDENCIES = [
    'fire==0.4.0',
    'numpy==1.21.4',
    'pandas==1.3.4',
    'python-dateutil==2.8.2',
    'pytz==2021.3',
    'six==1.16.0',
    'termcolor==1.1.0',
]

setup(
    name='datels',
    version=VERSION,
    description=SHORT_DESCRIPTION,
    author='joe-yama',
    author_email='s1r0mqme@gmail.com',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
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
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)