<img alt="OQ-CATK - The Earthquake Catalogue Toolkit (Lite Version)" class="right" style="width: 60%" src="https://raw.githubusercontent.com/klunk386/CatalogueTool-Lite/master/Logo/OQ-CATK-Logo.png" />

[![AGPLv3](https://www.gnu.org/graphics/agplv3-88x31.png)](https://www.gnu.org/licenses/agpl.html)

[Contribution guidelines for this project](Logo/OQ-CATK-Logo.png)

# OQ-CATK (Lite Version)

A simplified Python toolkit for earthquake catalogue manipulation and homogenisation

The toolkit consists of 11 main modules:
  * **Catalogue** - The main module for database manipulation an I/O
  * **Parsers** - Ad-hoc parsers for specific catalogues and bulletins (ISC, GCMT...)
  * **Selection** - Functions for high-level manipulation of catalogue objects
  * **Exploration** - Functions to explore database information and perform basic statistical analysis
  * **Regressor** - Utilities for magnitude conversion and catalogue homogenisation
  * **Declusterer** - Aftershock/Foreshock removal algorithms
  * **Seismicity** - Functions to calculate rates and occurrence relationships
  * **MagRules** - Library of magnitude conversion functions
  * **MapTools** - Utility to plot earthquake datasets on a map
  * **IscWeb** - API to download isf catalogues from the ISC web
  * **IscCode** - ISC agency code list

### Dependencies

OQ-CATK requires the following dependencies:

  * [NumPy/Scipy](http://www.scipy.org/)
  * [Matplotlib](http://matplotlib.org/)
  * [Basemap](http://matplotlib.org/basemap/)

### License

Copyright (c) 2017 GEM Foundation

OQ-CATK is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

You should have received a copy of the GNU Affero General Public License with this download. If not, see <http://www.gnu.org/licenses/>

### Disclaimer

The software provided herein is released as a prototype implementation on behalf of scientists and engineers working within the GEM Foundation (Global Earthquake Model).

It is distributed for the purpose of open collaboration and in the hope that it will be useful to the scientific, engineering, disaster risk and software design communities.

The software is NOT distributed as part of GEM’s OpenQuake suite (http://www.globalquakemodel.org/openquake) and must be considered as a separate entity. The software provided herein is designed and implemented by scientific staff. It is not developed to the design standards, nor subject to same level of critical review by professional software developers, as GEM’s OpenQuake software suite.

Feedback and contribution to the software is welcome, and can be directed to the hazard scientific staff of the GEM Model Facility (hazard@globalquakemodel.org).

The Catalogue Toolkit is therefore distributed WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

The GEM Foundation, and the authors of the software, assume no liability for use of the software.
