'''
Basic parts such as variable and data settings and operations.
'''
from IPython.display import clear_output
import os
import datetime
#import joblib

class Base():
    def __init__(self):
        # Working directory settings
        ## Mainly used in Tdp_reader
        self.working_directory = ""
        self.data = {}
        self.FIXED_RAW_DATA = {}
        self.key = []

        ## Mainly used in Missing
        self.preprocessing_data = {}
        self.latest_preprocessed_data = {}

        ## Mainly used in DataScience
        self.analyzing_data = {}
        self.objective_variable = {}
        self.split_data = {}
        self.model = {}

    def set_preprocess_key(self, *args):
        self.preprocessing_data = {}
        for key in args:
            if key in self.key: self.preprocessing_data[key] = self.data[key]
            else: print(f'{key} が見つかりません。 \nself.key で確認してください。')
        if len(args) == 0: self.preprocessing_data = self.data


    def set_analyze_key(self, *args):
        self.analyzing_data = {}
        for key in args:
            if key in self.key:
                if len(self.preprocessing_data.keys()) == 0: self.analyzing_data[key] = self.data[key]
                else : self.analyzing_data[key] = self.preprocessing_data[key]
            else : print(f'{key} が見つかりません。 \nself.key で確認してください。')
        if len(args) == 0: self.analyzing_data = self.data
        self.set_objective_variable()

    def set_objective_variable(self):
        for key in self.analyzing_data.keys():
            if 'objective_variable' in self.analyzing_data[key].columns:
                self.objective_variable[key] = 'objective_variable'
            else :
                clear_output()
                print(f"{f'[now data is {key}]': ^40}")
                print('---------Set objective variable---------')
                columns = self.analyzing_data[key].columns
                for index_c in range(len(columns)):
                    print(f'{index_c: <4} : {columns[index_c]}')
                num = input('Select number : ')
                num = int(num)
                self.objective_variable[key] = columns[num]

    def save(self):
        dt = datetime.datetime.now()
        date_name = f'{dt.year}_{dt.month}_{dt.day}_{dt.hour}_{dt.minute}_{dt.second}'

        if not os.path.exists(f'{self.working_directory}/preprocess_data_folder'): os.mkdir(f'{self.working_directory}/preprocess_data_folder')

        folder_path = f'{self.working_directory}/preprocess_data_folder/{date_name}'
        os.mkdir(folder_path)
        for key in self.key:
            if key in self.latest_preprocessed_data.keys(): self.latest_preprocessed_data[key].to_csv(f'{folder_path}/preprocessed_{key}.csv', index_label = False)
            else: self.data[key].to_csv(f'{folder_path}/{key}.csv', index_label = False)
