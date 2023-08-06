# SheetsORM
SheetsORM is a simple micro ORM extension for gspread.

Features:
- Create a entity class for each worksheet
- Columns are mapped to attributes
- Repository: Add,Remove,Update operations
- Type checking for attributes

## Requirements
Python 3.9+

## Installation

```
pip install sheetsorm
```


## Basic usage

1.[Create credentials in Google API Console](https://docs.gspread.org/en/latest/oauth2.html)

2.Creating an instance:
```python

from sheetsorm.orm import SheetsORM

# Create a SheetsORM instance
gs = SheetsORM(scope=['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive'],
        credentials_file='./credentials.json', # pass the path of the credentials file, or google drive URL 
        is_url=False, # True if the credentials file is a google drive URL
        spreadsheet_name='DEV' # pass the name of the spreadsheet
        )

# if the spread sheet is not found, it will be created
gs.connect()

# You should share the spreadsheet with your preferred email address
gs.share('your@email.com','user','owner')
```

3.Create a class for each worksheet:
```python
from sheetsorm.decorators import entity, column
from datetime import datetime

# define the entity
# the worksheet name by default is the class name
@entity(worksheet='Kat')
class Kat:
    # our primary key auto_increment with non-nullable values
    # name defines the column name in the worksheet, by default it is the attribute name
    id = column(int,name='ID',primary_key=True,increment=True, required=True)
    # pass the length of the column as argument to 'str'
    name = column(str(200),name='NAME',required=True)
    # or use as a string 
    color = column('20',name='COLOR')


# the entity decorator add a new constructor that allows you to create an instance
# from key values
meow  = Kat(name='Meow',birth_date=datetime(2019,1,1),color='black')

repo = gs.get_repository(Kat)

# add the object
repo.add(meow)
# and then commit the changes
repo.commit()

# pass lambda function to filter the results
find_meow = repo.find(lambda x: x.name=='Meow')
if len(find_meow) == 1:
    print('I Found Meow')
    print(f'His id: {find_meow[0].id}')
    print(f'His name: {find_meow[0].name}')
    print(f'His birth date: {find_meow[0].birth_date}')
    print(f'His color: {find_meow[0].color}')
else:
    print('I did not find Meow')


meow = find_meow[0]
meow.name = 'Meow2'
# Runtime type checkings
# meow.color  = 1  # TypeError: color must be of type 'str'
repo.update(meow)
repo.commit()

# Remove the row from the worksheet
repo.remove()
repo.commit()

# Other functions to use:
# repo.all(lambda x: x.color=='orange')
# repo.any(lambda x: x.name=='Mr. Potato')
```