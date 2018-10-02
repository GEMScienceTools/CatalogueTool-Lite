# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (C) 2017-2018 GEM Foundation
#
# OpenQuake is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenQuake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake. If not, see <http://www.gnu.org/licenses/>.

import sys
from setuptools import setup, find_packages

if sys.version_info < (3, 6):
    sys.exit('Sorry, Python < 3.6 is not supported')

url = "https://github.com/GEMScienceTools/CatalogueTool-Lite"

README = """
A simplified Python toolkit for earthquake catalogue manipulation and homogenisation

The toolkit consists of 12 main modules:

 * Catalogue - The main module for database manipulation an I/O
 * Parsers - Ad-hoc parsers for specific catalogues and bulletins (ISC, GCMT...)
 * Selection - Functions for high-level manipulation of catalogue objects
 * Exploration - Functions to explore database information and perform basic statistical analysis
 * Regressor - Utilities for magnitude conversion and catalogue homogenisation
 * Declusterer - Aftershock/Foreshock removal algorithms
 * Seismicity - Functions to calculate occurence rates and fit magnitude-frequency distributions
 * MagRules - Library of magnitude conversion functions
 * MapTools - Utility to plot earthquake databases on a map
 * Converters - Utility to convert to other formats
 * IscWeb - API to download isf catalogues from the ISC web
 * IscCode - ISC agency code list

"""

setup(
    name='OQCatk',
    version='0.1.0',
    description="""A simplified Python toolkit for earthquake catalogue
                   manipulation and homogenisation""",
    long_description=README,
    url=url,
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'basemap',
    ],
    author='GEM Foundation',
    author_email='hazard@globalquakemodel.org',
    maintainer='GEM Foundation',
    maintainer_email='hazard@globalquakemodel.org',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
    ),
    keywords="seismic hazard",
    license="AGPL3",
    platforms=["any"],
    package_data={"OQCatk": [
        "README.md", "LICENSE"]},
    include_package_data=True,
    zip_safe=False,
)
