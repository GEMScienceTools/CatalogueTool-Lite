# CatalogueTool-Lite
A simplified toolkit for earthquake catalogue handling
## 1 - Main Catalogue Object
A catalogue object can be instanciated using the *Database* class in the *Catalogue* library:
~~~
import Catalogue as Cat
Db0 = Cat.Database('Some Name (Optional)','Some Information (Optional)')
~~~

### 1.1 - Attributes
The most important attributes of the catalogue objects are the *Header* and *Events* variables. While *Header* is basically just a dictionary for general information about the catalogue (e.g. name, some descrition...), *Events* is the actual database (as list) of earthquake records, with a more complex internal structure.
Each element of the *Events* list is practically a dictionary containing data of an single event, grouped in four main keys: *Id*, *Magnitude*, *Location* and *Log*.
Here is an example:
~~~python
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
               'Prime': True}],
 'Magnitude': [{'MagCode': 'EMEC',
                'MagSize': 5.0,
                'MagError': None,
                'MagType': 'Mw'},
                {'MagCode': 'ISC',
                'MagSize': 4.9,
                'MagError': 0.1,
                'MagType': 'Ms'}],
 'Log': 'MERGED(EMEC Africa:1234);PREID(1111);'}
~~~
As it can be seen from the example, *Location* and *Magnitude* are also list of dictionaries. Each elements of those lists represents a separate solution from a particular agency.
*Log* is jut a container for processing information (explained later), although it could be used to store any arbitrary text data.
In the example above, the event *02000* contains two independent magnitude solutions, but only one location solution.

### 1.2 - Methods
Several methods for database manipulation, I/O and exploration are available:
  * *AddEvent* - Add an earthquake event to the database
  * *DelEvent* - Remove an earthquake avent from the database
  * *Import* - Import catalogue from file (csv format)
  * *Export* - Export catalogue to file (csv format)
  * *Load* - Import database structure from binary file (cPickle compressed)
  * *Dump* - Exprot database structure to binary file (cPickle compressed)
  * *Filter* - Filter earthquake events by key field and rule
  * *Extract* - Extract database information by key field
  * *KeyStat* - Compute statistics on key field occurrence
  * *Copy* - Create hardcopy of the database
  * *Append* - Concatenate event list of two databases
  * *Size* - Output number of earthquake events
  * *Print* - Print event information on screen (by ID or index)
  * *Sort* - Sort events according to origin time
  * *SetField* - Set database key field to a specific value
  * *GetIndex* - Get event index from ID string
  * *SetID* - Regenerate progressive IDs

### 1.3 - Catalogue I/O
Once instantiated an catalogue object, the database can be inflated manually (element by element) or by parsing an external source file. A parsed catalogue can also be manually augmented with new information.
For example, database items can be created in this way:
~~~python
import Catalogue as Cat
Db = Cat.Database('MyCat')

L = [{'Year': 1961, 'Month': 12, 'Day': 3, 'Hour': 5, 'Minute': 20, 'Second': 10}},
     {'Year': 1962, 'Month': 2, 'Day': 5, 'Hour': 12, 'Minute': 6, 'Second': 5}]

M = [{'MagCode': 'AAA', 'MagSize':5, 'MagError': 0.1, 'MagType':'Mw'},
     {'MagCode': 'BBB', 'MagSize':7, 'MagError': 0.2, 'MagType':'ML'}]

# Creating an new empty catalogue item
Db.AddEvent('E001')

# Creating a new item with just Location information
Db.AddEvent('E002', Location=L)

# Creating a new item with Location and Magnitude information
Db.AddEvent('E003', Location=L, Magnitude=M)

# Adding new information to an existing item
Db.AddEvent('E001', L, [], Append=True)
Db.AddEvent('E002', Magnitude=M, Append=True)

# Remove an existing item (by ID)
Db.DelEvent('E003')
~~~
Using all fields