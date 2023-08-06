#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 01/08/2020
           """

__all__ = []


def test_import():
    import munin

    print(munin.__version__)


def test_import_samples():
    from munin.generate_report import generate_html

    print(generate_html.__doc__)
