from typing import Callable, Generic, List, TypeVar, Any
from collections import namedtuple
import datetime
import gspread
import pandas as pd
from pandas.core.frame import DataFrame
from .util import DTYPES


T  = TypeVar('T')
nullable_values = {
    'str': '',
    'int': 0,
    'float': 0.0,
    'bool': False,
    'date': '',
    'datetime': '',
    'time': None,

}
class Repository(Generic[T]):
    def __init__(self, worksheet: gspread.models.Worksheet, model):
        """
        Repository is a class that helps you to manage your data in a google sheet.
        It's a generic class that works with any object that has a namedtuple.

        ### Parameters
        worksheet (gspread.models.Worksheet): The worksheet that you want to manage
        model: The model that you want to use to manage the data.
        """
        self.worksheet  = worksheet
        self.model = model
        self.pending = []
        self.primary_key = [x for x in self.model['__data'] if x['primary_key'] == True]
        self.primary_key_attr  = self.primary_key[0]['attribute'] if len(self.primary_key) >0 else None
        self.primary_key_name  = self.primary_key[0]['name'] if len(self.primary_key) >0 else None
        self.is_autoincrement  = self.primary_key[0]['increment'] if len(self.primary_key) >0 else None
        self.name_to_attribute = {x['name']: x['attribute'] for x in self.model['__data']}
        self.attribute_to_name = {x['attribute']: x['name'] for x in self.model['__data']}
        
    def _get_attribute_by_name(self, attr,value):
        """
        Get the attribute casted to the correct type

        ### Parameters
        attr (dict): The attribute of the model
        value (str): The value of the cell
        """

        if value == '' or value == 'null' or value == None:
            if attr['required']:
                raise ValueError(f'{attr["name"]} cannot be null')
            return nullable_values[attr['dtype']]

        if attr['dtype'] == 'int':
            return int(value)
        elif attr['dtype'] == 'str':
            # get the lenthg of the varchar
            length = attr['length']
            value = str(value)
            if len(value) > int(length):
                Exception('Value is too long')
            return value[0: int(length)]
        elif attr['dtype'] == 'datetime':
            value = str(value)
            return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        elif attr['dtype'] == 'bool':
            return bool(value == '1' or value == 'True')    
        elif attr['dtype'] == 'float':
            return float(value)
        else:
            raise Exception('Unsupported type -> ', attr['dtype'], f'"{value}"')
    
    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert the repository to a pandas dataframe
        """
        temp_df  = DataFrame({
            column['name']: pd.Series(dtype=DTYPES[column['dtype']]) for column  in self.model['__data']
        })

        temp_df = temp_df.append(pd.DataFrame(self.worksheet.get_all_records()))
        temp_df = temp_df.applymap(lambda x: None if x in ['null',''] else x)
        temp_df = self._apply_columns_types(temp_df)
        return temp_df

    def _sheet_row_to_object(self, row: dict):
        """
        Convert the row of the sheet to a namedtuple
        """
        obj = None
        obj = namedtuple(self.worksheet.title, ' '.join([x['attribute'] for x in self.model['__data']]))
        # "<Table(id='%d', name='%s')>"
        # dinamic namedtuple
        for attr in self.model['__data']:
            setattr(obj,attr['attribute'],self._get_attribute_by_name(attr,row[attr['name']]))
        return obj
    
    def _object_to_dict(self, obj: T, primary_key = False) -> dict:
        """
        Convert the object to a dict
        """
        return {attr['name']: getattr(obj, attr['attribute']) for attr in self.model['__data'] if primary_key and  attr['primary_key'] or not attr['primary_key']}
    
    def _apply_columns_types(self,_df: pd.DataFrame):
        """
        Apply the column types to the dataframe
        """
        df = _df.copy()
        date_columns = [x['name'] for x in self.model['__data'] if x['dtype'] in ['datetime']]
        
        for column in df.columns:
             if column in date_columns:
                df[column] = pd.to_datetime(df[column])
             else:
                df[column] = df[column].astype(df[column].dtype)
        return df
    
    def get_all(self) -> List[T]:
        """
        Query all the data in the repository
        """
        return [self._sheet_row_to_object(row) for row in  self.worksheet.get_all_records()]

    def add(self, obj: T):
        """
        Add a object on the repository
        """
        self.pending.append({'operation': 'add', 'obj': obj})
    
    def remove(self, obj: T):
        """
        Remove a object from the repository
        """
        self.pending.append({'operation':'delete', 'obj':obj})
    
    def update(self, obj: T):
        """
        Update a object on the repository
        """
        # check if the object is in the pending updates
        search = [getattr(x['obj'], self.primary_key_attr) == getattr(obj, self.primary_key_attr) for x in self.pending]
        if not any(search):
            self.pending.append({'operation':'update', 'obj': obj})
        else:
            # update the object
            self.pending[search.index(True)] = {'operation':'update', 'obj': obj}

    def find(self, call: Callable):
        """
        Query the repository with a callable
        """
        df = self.get_all()
        return [x for x in df if call(x)]
    
    def any(self, call: Callable):
        """
        Query the repository with a callable if any of the objects return True
        """
        return any(call(x) for x in self.get_all())
    
    def all(self, call: Callable):
        """
        Query the repository with a callable if all of the objects return True
        """
        return all(call(x) for x in self.get_all())
    
    def count(self, call: Callable):
        """
        Count the number of rows
        """
        return len([x for x in self.get_all() if call(x)])
    
    def get_byid(self, id: Any) -> T:
        """
        Query the repository by id

        You must declare a primary key on the model
        """
        return self.find(lambda x: getattr(x, self.primary_key_attr) == id)[0]
    
    def _update_cells(self, df: pd.DataFrame):
        """
        Update the cells of the the worksheet using gspread
        """
        # add the row
        self._df_copy = df.copy()
        self._df_copy = self._apply_columns_types(self._df_copy)

        for x in  self._df_copy.select_dtypes(include=['datetime64','datetime64[ns]','<M8[ns]']).columns.tolist():
            self._df_copy[x] = self._df_copy[x].apply(lambda x: None if pd.isnull(x) else x.strftime('%Y-%m-%d %H:%M:%S'))
        self._df_copy = self._df_copy.fillna('null')
        self.worksheet.update([self._df_copy.columns.values.tolist()] + self._df_copy.values.tolist())
    
    def clear(self,):
        """
        Clear the intire worksheet
        ### [NOT IMPLEMENTED]

        This will delete all the data in the worksheet
        """
        # self.worksheet.clear()
    
    def commit(self):
        """
        Commit the pending changes
        """
        # load the dataframe
        df = self.to_dataframe()
        self.primary_key_name = self.primary_key_name

        for operation in self.pending:
            obj  = operation['obj']
            if operation['operation'] == 'add':
                # check if the primary key already exists
                if df[self.primary_key_name].isin([getattr(obj,self.primary_key_attr)]).any():
                    raise Exception('Primary key already exists')
                
                # get the name of the columns
                # las id
                self.worksheet.add_rows(1)
                last_id = 0 if pd.isna(df[self.primary_key_name].max()) else df[self.primary_key_name].max()
                new_dict = self._object_to_dict(obj)
                if self.is_autoincrement:
                    new_dict[self.primary_key_name] = last_id + 1
                df = df.append(new_dict, ignore_index=True)        
                self._update_cells(df)
            elif operation['operation'] == 'delete':
                # get the name of the columns
                primary_key_value = getattr(obj,self.primary_key_attr)
                # remove the row
                self.worksheet.delete_rows(df[df[self.primary_key_name] == primary_key_value].index.tolist()[0]+2)
                df.drop(df[df[self.primary_key_name] == primary_key_value].index, inplace=True)

                # df = df[df[primary_key] != primary_key_value]
            elif operation['operation'] == 'update':
               # check the primary key
                if getattr(obj,self.primary_key_attr) == None:
                    raise Exception('Primary key is not set')
                # check if the primary key if not exists
                if not df[self.primary_key_name].isin([getattr(obj,self.primary_key_attr)]).any():
                    raise Exception('Primary key does not exists')
                
                # get the name of the columns
                new_dict = self._object_to_dict(obj,primary_key=True)
                # update the row
                df.loc[df[self.primary_key_name] == getattr(obj,self.primary_key_attr), new_dict.keys()] = new_dict.values()
                self._update_cells(df)
            else:
                raise Exception('Unsupported operation -> ', operation['operation'])
        self.pending = []

        
        
