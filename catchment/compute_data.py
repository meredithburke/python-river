"""Module containing mechanism for calculating standard deviation between datasets.
"""

import glob
import os
import pandas as pd

from catchment import models, views

class CSVDataSource:
    def __init__(self, data_dir, dataset):
        self.data_dir = data_dir
        self.dataset = dataset

    def load_catchment_data(self):
        data_file_paths = glob.glob(os.path.join(self.data_dir, self.dataset))
        if len(data_file_paths) == 0:
            raise ValueError('No CSV files found in the data directory')
        return list(map(models.read_variable_from_csv, data_file_paths))
    
class JSONDataSource:
    def __init__(self, data_dir, dataset):
        self.data_dir = data_dir
        self.dataset = dataset

    def load_catchment_data(self):
        data_file_paths = glob.glob(os.path.join(self.data_dir, self.dataset))
        if len(data_file_paths) == 0:
            raise ValueError('No JSON files found in the data directory')
        return list(map(models.read_variable_from_json, data_file_paths))

def daily_std(dataset):
    """Calculate the standard deviation"""
    return dataset.groupby(dataset.index.date).std()

def compute_standard_deviation_by_day(data):
    """Calculate the standard deviation"""
    daily_std_list = []
    daily_std_list = map(daily_std, data)
    daily_standard_deviation = pd.concat(daily_std_list)
    return daily_standard_deviation

def analyse_data(data_source):
    """Calculate the standard deviation by day between datasets.

    Gets all the measurement data from the CSV files in the data directory,
    works out the mean for each day, and then graphs the standard deviation
    of these means.
    """
    data = data_source.load_catchment_data()
    return compute_standard_deviation_by_day(data)
