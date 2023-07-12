# -*- coding: utf-8 -*-

# Copyright (c) 2023 Javier Escalada Gómez
# All rights reserved.
# License: BSD 3-Clause Clear License (see LICENSE for details)

import unittest
import doctest
import templite.doctest_utils as doctest_utils
import templite

"""
It loads the [doctest](https://docs.python.org/3/library/doctest) and [expose
them as unittests](https://docs.python.org/3/library/doctest.html#unittest-api).
"""

def load_tests(loader, tests, ignore):
    parser = doctest_utils.MarkdownDocTestParser()
    test_finder = doctest.DocTestFinder(parser=parser)
    tests.addTests(doctest.DocTestSuite(templite, test_finder=test_finder))
    tests.addTests(doctest.DocFileSuite("../README.md.in",
                                        globs=templite.__dict__,
                                        parser=parser))
    return tests
