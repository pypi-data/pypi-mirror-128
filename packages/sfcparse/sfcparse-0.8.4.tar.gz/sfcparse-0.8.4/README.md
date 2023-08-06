# sfcparse Module for Python
### sfcparse = Simple File Configuration Parse
### Current version 0.8.4
See "Updates" section on bottom for the latest version information
___
### Introduction
This module allows you to import and create custom python style save/config files for your program or script on a plain text file with any file extension. **It can be used to easily export any data to a file as well**. Also contains a feature for easily formatting data types for clean multiline output when exporting data to files, **and importing is more secure than importing your values from .py files**. 

### Goal for the Project:
To provide an easy alternative to using save/config files in an attempt to customize importing python data and saving any data to files for your projects simple. This also gives you the universal freedom to use any file extension or any made up file type you want, and ensures importing from your file to retrieve values is more secure than importing your values from .py files.

### Importing (Python only):
Imports stored variable names and their assigned values from any text file.

Returns a class with attributes from the file keeping python's natural recognition of data types, including comment lines being ignored.

**Accepted Imported Data Types:**
str, int, float, bool, list, dict, tuple, set, nonetype, bytes

### Exporting/Appending:
It simply sends string data to a file. It may be used for any string data file output.

### Formatting:
Simply formats any dict, list, set, or tuple to a clean multiline structure, and return it as str. It can be
exported to a file neatly.
___

# Tutorial Videos (New):
Quick Start Tutorial: [YouTube Video](https://youtu.be/W7TIVFE7epI)

Full Training Series: [YouTube Playlist](https://www.youtube.com/watch?v=7-_iRNAQkno&list=PLaVLtZTXV5i2Zkj704h-Cxl3uDqrFpohU&index=1)

___

# Tutorial: Install & Usage
```python
pip install sfcparse
```

# Usage: Importing
#### Imports Pythonic Data Types from your Text File

**Example test file**
Python data inside a file called **settings.config**.
```ini
# Comment for Single Line Data
saved_str = 'John Doe'
saved_int = 1024
saved_float = 128.75
saved_bool = False
saved_list = [1, 2, 3]
saved_dict = {'key1': 1, 'key2': 2}
saved_tuple = (1,2,3)
saved_set = { 1, 2, 3 }


# Comment for Multiline Data Sets
saved_data_multiline_dict = {
    'key1' : 'value 1',
    'key2' : 'value 2',
    'key3' : 'value 3'
}

saved_data_multiline_tuple = (
    1,
    2,
    3
)
```
### Importing the above file into your python project and accessing the data
```python
import sfcparse

settings_file = sfcparse.importfile('settings.config')

# Access any values imported
settings_file.saved_str
settings_file.saved_list
settings_file.saved_data_multiline_dict['key1']
...
```
### That's it!
___
# Usage: Exporting - Single Line Values
#### Writes/Overwrites a New File

Exporting data to example file **settings.config**.

**Note** these are just examples to build your data to export.
```python
import sfcparse

export_file = sfcparse.exportfile

# Single Line Values
string_to_save = 'John Doe'
number_to_save = 64
tuple_to_save = (1,2,3)


# Final Data to Export
data_to_save = f'''
# Comment Line
string_to_save = '{string_to_save}'
number_to_save = {number_to_save}
tuple_to_save = {tuple_to_save}
'''

export_file('settings.config', data_to_save)
```
### This will be the expected output stored to the file
```ini
# Comment Line
string_to_save = 'John Doe'
number_to_save = 64
tuple_to_save = (1,2,3)
```
### That's it!
___
# Usage: Exporting - Multiline Values
#### Writes/Overwrites a New File

Exporting data to example file **settings.config**.

**Note** these are just examples to build your data to export.
```python
import sfcparse

export_file = sfcparse.exportfile

string_to_save = 'John Doe'
number_to_save = 64

# Multiline Values
dict_to_save = """{

    'key1' : 'value1',
    'key2' : 'value2'    
}
"""

list_to_save = """[

    1,
    2,
    3
]
"""

# Dict with Vars - NOTE: Must escape Curly Braces if using variables via f-string
dict_to_save_vars = f"""{{

    'key1' : '{string_to_save}',
    'key2' : {number_to_save}
}}
"""


# Final Data to Export
data_to_save = f'''
# Comment Line
dict_to_save = {dict_to_save}
list_to_save = {list_to_save}
dict_to_save_vars = {dict_to_save_vars}
'''

export_file('settings.config', data_to_save)
```
### This will be the expected output stored to the file
```ini
# Comment Line
dict_to_save = {

    'key1' : 'value1',
    'key2' : 'value2'    
}

list_to_save = [  

    1,
    2,
    3
]

dict_to_save_vars = {

    'key1' : 'John Doe',
    'key2' : 64
}
```
## Clean Format: You can also use "cleanformat" to easily organize your multiline output
```python

data_to_save_clean = {'key1':'value1', 'key2':'value2', 'key3':'value3'}

clean_output = sfcparse.cleanformat(data_to_save_clean)

export_file('settings.config', f"data_to_save_clean = {clean_output}")
```
### This will be the clean expected output stored to the file
```ini
data_to_save_clean = {
    'key1' : 'value1',
    'key2' : 'value2',
    'key3' : 'value3'
}
```

### That's it!
___
# Usage: Appending:
#### Writes New Data to a File if it Exists

It is the same syntax as exporting, but here is an example using the same exported output from "Exporting - Single Line" **settings.config**.

**Note** these are just examples to build your data to append.

**Also** Single line appending may be more tedious than multiline, so it is recommended to build your data with multiple lines as shown!
```python
import sfcparse

append_file = sfcparse.appendfile

data_to_append = ['item1', 'item2', 'item3']
data_to_append2 = [1,2,3]

# Single Line Appending
append_file('settings.config', f"data_to_append = {data_to_append}")

# Multiline Appending
final_save_data = f"""
data_to_append = {data_to_append}
data_to_append2 = {data_to_append2}
"""

append_file('settings.config', f"data_to_append = {final_save_data}")
```
### This will be the expected output appended to the file if using the multiline append method
```ini
# Comment Line
string_to_save = 'John Doe'
number_to_save = 64
tuple_to_save = (1,2,3)
data_to_append = ['item1', 'item2', 'item3']
data_to_append2 = [1,2,3]
```
### That's it!

___
# Module Performance
### Importing
Imported a file 1000 times with 100 lines of data in 0.6s.

##### Lab Test Conducted:

```python
from sfcparse import importfile
import time

file_to_import = 'data.test'
num_of_tests = 1000

# Performance Test
start_time = time.perf_counter()
for i in range(num_of_tests):
    importfile(file_to_import)
end_time = time.perf_counter()

elapsed_time = (end_time - start_time)

print(elapsed_time)
```
##### System: Tested on a 4th-Gen Intel Core i7-4790 at 3.6GHz
___

# Updates - sfcparse v0.8.0

**API change:**
- **NEW: v0.8.0** - Compatible only on Python version 3.6+
- **PREVIOUS: v0.7.7** - Compatible only on Python version 3.0+

**Performance changes:**
- cleanformat:
    - code improvement has a 23% performance gain
- importfile:
    - code improvement has a 10% performance gain

**Feature Additions:**
- cleanformat:
    -  Has a new indentation level feature to add custom indent levels for exporting to a file
    **NOTE**: formatting performance will **gain 5% boost if you set indent level to 0 (Default 1)**.
    **Performance will decrease** with more levels of indentation added.
    - Now supports nested data sets, but will not apply indentation to sub-level data sets
    - Now does not parse commas in values or keys and retains its original representation
- importfile:
    - Now supports importing nested data sets even when subsets are on multiple lines in the file
    - Comments can now be added after a value

**General:**
- Updated comments in module/functions

- 0.8.3:
    - Fixed Importing and Appending error exceptions not raising correctly when checking if file exists
- 0.8.4
    - Added Type Hinting and Return Hinting to improve readability

# Known Limitations
**Importing**
 - Does not support importing unpacked variables and values
 - Does not support importing variables as values


# Future Upgrades
**Importing**
- Add support for importing variables as values
- Add support for unpacked variables and values