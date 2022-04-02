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
from templite import __version__

setup(
    name='templite',
    version=__version__,
    url='https://github.com/Kerrigan29a/templite.git',
    author='Javier Escalada Gómez',
    author_email='kerrigan29a@gmail.com',
    description='A light-weight, fully functional, general purpose templating engine',
    packages=find_packages(),    
    install_requires=[],
    license='GNU GPLv3',
    entry_points={
        'console_scripts': [
            'templite=templite:main',
        ],
    },
)
