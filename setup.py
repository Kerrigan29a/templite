# Copyright (c) 2022 Javier Escalada Gómez
# All rights reserved.
#
# Based on Templite+ by Thimo Kraemer <thimo.kraemer@joonis.de>
# Copyright (c) 2009 joonis new media
# From: http://www.joonis.de/de/code/templite
#
# Based on Templite by Tomer Filiba
# From: http://code.activestate.com/recipes/496702/
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.

from setuptools import setup, find_packages
from pathlib import Path
from templite import __version__, __author__, __email__, __license__, __doc__

base = Path(__file__).parent
long_description = (base / "README.md").read_text()

setup(
    name='templite',
    version=__version__,
    url='https://github.com/Kerrigan29a/templite',
    project_urls={
        "Source": "https://github.com/Kerrigan29a/templite",
    },
    author=__author__,
    author_email=__email__,
    description=__doc__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    license=__license__,
    entry_points={
        'console_scripts': [
            'templite=templite:main',
        ],
    },
    # From https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities",
    ],
    platforms="any",
    keywords=["template"],
)
