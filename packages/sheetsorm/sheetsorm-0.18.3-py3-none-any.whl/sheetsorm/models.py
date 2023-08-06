from typing import  TypedDict



class Column(TypedDict):
    """
    Column is a TypedDict that represents a column in a table.

    It has the following keys:
    - name: the name of the column
    - attribute: the attribute in the model that corresponds to the column
    - dtype: the type of the column (int,str,datetime.datetime,)
    - primary_key: whether the column is a primary key
    - length: the length of the column
    - required: whether the column is required
    """
    attribute : str
    name: str
    dtype : str
    length : int
    primary_key : bool
    required: bool


