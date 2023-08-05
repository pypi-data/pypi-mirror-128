'''

'''
import pandas as pd
import numpy as np
from copy import deepcopy
from pytdp.reader.api import (
    Tdp_reader
)


# Deletes column information with missing values greater than a certain value (input type [pandas.core.frame.DataFrame])
def delete_null_df(dataframe:pd.core.frame.DataFrame, null_label = np.nan, percent:int = 80) -> pd.core.frame.DataFrame:
    # Treat the case of a specific string as a missing value
    if type(null_label) == str: return dataframe.drop(dataframe.columns[((dataframe == null_label).sum()/len(dataframe) > percent).values], axis = 1)
    else:
        # Treating a specific number as a missing value
        if np.isnan(null_label): return dataframe.drop(dataframe.columns[(dataframe.isnull().sum()/len(dataframe) > percent).values], axis = 1)
        # Treating a specific number as a missing value
        else: return dataframe.drop(dataframe.columns[((dataframe == null_label).sum()/len(dataframe) > percent).values], axis = 1)

# Deletes column information with missing values greater than a certain value (input type [dict])
def delete_null(data_dict:dict, null_label = np.nan, percent:int = 80) -> dict:
    for df_key in data_dict.keys(): data_dict[df_key] = delete_null_df(data_dict[df_key], null_label, percent)
    return data_dict

class Missing(Tdp_reader):
    def __init__(self, data_list_or_directory, working_directory):
        super(Missing, self).__init__(data_list_or_directory, working_directory)

    # Deletes column information with missing values greater than a certain value (input type [pandas.core.frame.DataFrame])
    def delete_null_df(self, dataframe:pd.core.frame.DataFrame, null_label = np.nan, percent:int = 80) -> pd.core.frame.DataFrame:
        # Treat the case of a specific string as a missing value
        if type(null_label) == str: return dataframe.drop(dataframe.columns[((dataframe == null_label).sum()/len(dataframe) > (percent/100)).values], axis = 1)
        else:
            # Treating NULL as a missing value
            if np.isnan(null_label): return dataframe.drop(dataframe.columns[(dataframe.isnull().sum()/len(dataframe) > percent).values], axis = 1)
            # Treating a specific number as a missing value
            else: return dataframe.drop(dataframe.columns[((dataframe == null_label).sum()/len(dataframe) > (percent/100)).values], axis = 1)

    # Deletes column information with missing values greater than a certain value (input type [dict])
    def delete_null(self, null_label = np.nan, percent:int = 80) -> dict:
        if len(self.preprocessing_data.keys()) == 0: data = deepcopy(self.data)
        else : data = deepcopy(self.preprocessing_data)
        for df_key in data.keys():
            print(f'Delete_null : {df_key} ...', end = '')
            data[df_key] = self.delete_null_df(data[df_key], null_label = null_label, percent = percent)
            print('Complete !')
        self.delete_null_data = data
        self.update_preprocessed_data(data)

    # 加工でーたの更新
    def update_preprocessed_data(self, data):
        self.latest_preprocessed_data = data
        
