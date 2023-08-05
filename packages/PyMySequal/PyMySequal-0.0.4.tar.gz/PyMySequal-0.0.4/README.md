# Simple MySQL API For Python
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)                 
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)   


## Usage

- Make sure you have Python installed in your system.
- Run Following command in the CMD.
 ```
  pip install PyMySequal
  ```
## Example

 ```
from PyMySequal import get_records
get_records(Server,Database,Query)
```
## Arguments Definition 
 ```
 Server     --> Server Name
 Database   --> Database Name 
 Query      --> Sql Query
```

## Getting the Query in Varaiable 
 ```
eg. Query= ' Select id , name  \
             from Customer \
             Where id=1 '
```

## Note 
- get_records() function will get Server name , Database and Query as input

- All the Arguments (i.e) Server, database , query must be passed as String

- You can read the query in varaiable and further pass that varaiable as argument or else you can directly type query with multiple lines in one variable using \

- The Output will be in DataFrame