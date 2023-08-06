# Welcome to date_pick ⛏️
[![Codestyle: Black](https://img.shields.io/badge/codestyle-black-black.svg)](https://github.com/psf/black)
[![Codecheck: Flake8](https://img.shields.io/badge/codecheck-flake8-blue.svg)](https://gitlab.com/pycqa/flake8)

## Description

Pick date by conditions and list of re-like wildcards

## Quickstart
```
>>> from date_pick import DatePick
>>> import datetime
>>> 
>>> datetime.datetime.now()
datetime.datetime(2021, 11, 22, 15, 53, 20, 357911)
>>> 
>>> picker = DatePicker()
>>> # pick the nearest Monday 4 AM
>>> picker.pick(["*-*-*-0 04:00:00"])
"2021-11-29 04:00:00"
```

## Authors

* Nick Kuzmenkov