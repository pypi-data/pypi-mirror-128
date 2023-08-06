
<!--![munin](.github/images/munin.svg)-->

<p align="center">
  <img src=".github/images/munin.svg" alt='munin' />
</p>

<h1 align="center">Munin</h1>

<!--# Munin-->

```
Old Norse: Muninn
```

![python](.github/images/python.svg)

[![Build Status](https://travis-ci.com/pything/munin.svg?branch=master)](https://travis-ci.com/pything/munin) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) [![Coverage Status](https://coveralls.io/repos/github/pything/munin/badge.svg?branch=master)](https://coveralls.io/github/pything/munin?branch=master)
___
> Reporting.
___

This package is a package for generating classification reports. Uses jinja2 templates, see documentation.

# Quick Start

```
  pip install munin

```

Now you can add all your metrics and plots.

```
  from munin import generate_html
  from warg import NOD # used for generating a dict with the same keys as names in context

  ...

  metrics = NOD.dict_of(accuracy, precision, f1_score, recall, support).as_flat_tuples()

  bundle = NOD.dict_of(title, confusion_matrix, metrics, predictions)

  generate_html(file_name, **bundle)
```
