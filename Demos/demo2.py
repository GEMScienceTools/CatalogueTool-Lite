"""
DOWNLOADING ISC CATALOGUE
"""

from OQCatk import IscWeb as Iw

# Search Area
lon = [-20, 60]
lat = [-40, 40]

# Initializing the downloader
isc_url = Iw.ISCBulletinUrl()

# List available fields
isc_url.ListFields()

# Setting time period
isc_url.SetField('StartYear','2010')
isc_url.SetField('EndYear','2013')

# Setting magnitude threshold
isc_url.SetField('MinimumMagnitude','6.5')
isc_url.SetField('MaximumMagnitude','7.0')

# Search restricted to a buffer area
isc_url.SetField('SearchAreaShape','RECT')
isc_url.SetField('RectangleBottomLatitude',lat[0])
isc_url.SetField('RectangleTopLatitude',lat[1])
isc_url.SetField('RectangleLeftLongitude',lon[0])
isc_url.SetField('RectangleRightLongitude',lon[1])

# Using mirror web-site
isc_url.UseMirror()

# Type of catalogue and format
isc_url.SetField('OutputFormat','ISF')
isc_url.SetField('CatalogueType','REVIEWED')

# Performing download (split over two year blocks)
isc_url.GetCatalogue(SplitYears=2)

# Write catalogue to disk
isc_url.WriteOutput('data/isc-rev-africa.isf', OverWrite=True)
