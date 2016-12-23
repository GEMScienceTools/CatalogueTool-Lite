# CatalogueTool-Lite
A simplified toolkit for earthquake catalogue handling

## Main Catalogue Object
A catalogue database object is instanciated with:
~~~
import Catalogue as Cat
Db0 = Cat.Database('Some Name (Optional)')
~~~
The most important attributes of the catalogue objects are the *header* and the *events* variables. While *header* contains general information about the catalogue itself (e.g. name, descrition...), *events* is the actual database of earthquake records, in the form of a list.
Each element of the *events* list is a dictionary containing data of an single event, grouped by key: *Id*, *Magnitude*, *location* and *Log*:
~~~
{'Id': '02000',
 'Location': [{'LocCode': 'ISC',
               'Year': 1972,
               'Month': 1,
               'Day': 19,
               'Hour': 0,
               'Minute': 37,
               'Second': 7.5,
               'Longitude': -13.8138,
               'Latitude': 31.3611,
               'Depth': 33.0,
               'LatError': None,
               'LonError': None,
               'DepError': None,
               'SecError': 0.35,
               'Prime': True],
 'Magnitude': [{'MagCode': 'EMEC',
                'MagSize': 5.0,
                'MagError': None,
                'MagType': 'Mw'}],
 'Log': 'MERGED(EMEC Africa:116218);PREID(777017);'}
~~~
*Location* and *Magnitude* are then list of dictionaries. Each elements of the list represents a separate solution from a particular agency. *Log* is a container for processing information, although it can be used to store any arbitrary etxt data.