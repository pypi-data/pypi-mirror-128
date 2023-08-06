# datels

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/datels?style=plastic)](https://github.com/joe-yama/datels) [![PyPI - License](https://img.shields.io/pypi/l/datels?style=plastic)](https://github.com/joe-yama/datels) [![PyPI](https://img.shields.io/pypi/v/datels?style=plastic)](https://pypi.org/project/datels/)

`datels` is a simple CLI that displays a list of dates line by line.

## Installation

To install datels with pip, run: `pip install datels`

To install datels from source, first clone the repository and then run:
`python setup.py install`

## Basic Usage

```bash
$ datels --start 1994-03-07 --end 1994-03-10
19940307
19940308
19940309
```

if you want to specify formatting,

```bash
$ datels --start 1994-03-07 --end 1994-03-10 --format %Y/%m/%d
1994/03/07
1994/03/08
1994/03/09
```

The strftime to parse time, eg “%Y/%m/%d”. See strftime documentation for more information: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior.

By default, datels returns dates daily-based list. You can specify by using `--freq` option:

```bash
datels --start 1994-03-07 --end 1994-03-08 --format %Y/%m/%dT%H --freq H
1994/03/07T00
1994/03/07T01
1994/03/07T02
1994/03/07T03
1994/03/07T04
1994/03/07T05
1994/03/07T06
1994/03/07T07
1994/03/07T08
1994/03/07T09
1994/03/07T10
1994/03/07T11
1994/03/07T12
1994/03/07T13
1994/03/07T14
1994/03/07T15
1994/03/07T16
1994/03/07T17
1994/03/07T18
1994/03/07T19
1994/03/07T20
1994/03/07T21
1994/03/07T22
1994/03/07T23
```
