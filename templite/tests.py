# -*- coding: utf-8 -*-

# Copyright (c) 2023 Javier Escalada Gómez
# All rights reserved.
# License: BSD 3-Clause Clear License (see LICENSE for details)

import unittest
import doctest
import templite
import re

"""
It loads the [doctest](https://docs.python.org/3/library/doctest) and [expose
them as unittests](https://docs.python.org/3/library/doctest.html#unittest-api).
"""

class MarkdownTestParser(doctest.DocTestParser):
    """A DocTestParser that removes code blocks from Markdown files before
    parsing them. This allows to write Markdown files with code blocks that
    can be tested with doctest.
    """
    def parse(self, string, name='<string>'):
        string = re.sub(r'^\s*(```|~~~)\s*.*$', '', string, flags=re.MULTILINE)
        return super().parse(string, name)


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(templite))
    tests.addTests(doctest.DocFileSuite("../README.md.in",
                                        globs=templite.__dict__,
                                        parser=MarkdownTestParser()))
    return tests
