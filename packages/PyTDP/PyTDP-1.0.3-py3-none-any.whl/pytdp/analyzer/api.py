from pytdp.preprocessor.api import(
    Missing
)
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import numpy as np


class DataScience(Missing):
    def __init__(self, data_list_or_directory, working_directory):
        super().__init__(data_list_or_directory, working_directory)

    def check_analyzing_data(self):
        if len(self.analyzing_data.keys()) == 0:
            if len(self.latest_preprocessed_data.keys()) == 0:
                self.analyzing_data = self.data
                return self.data
            self.analyzing_data = self.latest_preprocessed_data
            return self.latest_preprocessed_data
        else: return self.analyzing_data

    def check_objective_variable(self):
        if len(self.objective_variable.keys()) == 0:
            self.set_objective_variable()

    def train_test_split(self, test_size = 0.25, train_size = 0.75):
        split_data = self.check_analyzing_data()
        self.check_objective_variable()
        for key in split_data.keys():
            self.split_data[key] = {}
            X = (split_data[key]).drop(self.objective_variable[key], axis = 1)
            y = split_data[key][self.objective_variable[key]]
            self.split_data[key]['X_train'], self.split_data[key]['X_test'], self.split_data[key]['y_train'], self.split_data[key]['y_test'] = train_test_split(X, y, test_size = 0.25, train_size = 0.75)


    def machine_learning(self, learning_model):
        for key in self.analyzing_data:
            model = learning_model()
            model.fit(self.split_data[key]['X_train'], self.split_data[key]['y_train'])
            y_pred = model.predict(self.split_data[key]['X_test'])
            self.model[key] = {}
            self.model[key]['y_predict'] = y_pred
            self.model[key]['mean_absolute_error'] = mean_absolute_error(self.split_data[key]['y_test'], y_pred)
            self.model[key]['mean_squared_error'] = mean_squared_error(self.split_data[key]['y_test'], y_pred)
            self.model[key]['root_mean_squared_error'] = np.sqrt(mean_squared_error(self.split_data[key]['y_test'], y_pred))
            self.model[key]['r2_score'] = r2_score(self.split_data[key]['y_test'], y_pred)
            self.model[key]['model'] = model
        print('Complete learning! Check [self.model]')
