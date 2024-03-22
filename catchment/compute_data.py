"""Module containing mechanism for calculating standard deviation between datasets.
"""

import glob
import os
import pandas as pd

from catchment import models, views

class CSVDataSource:
    def __init__(self, dir_path):
        self.dir_path = dir_path  

    def load_catchment_data(self):
        data_file_paths = glob.glob(os.path.join(self.dir_path, 'rain_data_2015*.csv'))
        if len(data_file_paths) == 0:
            raise ValueError('No CSV files found in the data directory')
        data = map(models.read_variable_from_csv, data_file_paths)
        return list(data)

class JSONDataSource:
    def __init__(self, dir_path):
        self.dir_path = dir_path  

    def load_catchment_data(self):
        data_file_paths = glob.glob(os.path.join(self.dir_path, 'rain_data_2015*.json'))
        if len(data_file_paths) == 0:
            raise ValueError('No JSON files found in the data directory')
        data = map(models.read_variable_from_json, data_file_paths)
        return list(data)  

class XMLDataSource:
    def __init__(self, dir_path):
        self.dir_path = dir_path  

    def load_catchment_data(self):
        data_file_paths = glob.glob(os.path.join(self.dir_path, 'rain_data_2015*.xml'))
        if len(data_file_paths) == 0:
            raise ValueError('No XML files found in the data directory')
        data = map(models.read_variable_from_xml, data_file_paths)
        return list(data)  

def daily_std(data):
    """Calculate the daily std of a 2D data array.
    Index must be np.datetime64 compatible format."""
    return data.groupby(data.index.date).std()

def compute_standard_deviation_by_day_map(data):
    """Replacing for loop with map"""
    daily_std_map=[]
    daily_std_map=map(daily_std, data)
    daily_standard_deviation = pd.concat(daily_std_map)
    return daily_standard_deviation

def analyse_data(data_source):
    """Calculate the standard deviation by day between datasets.

    Gets all the measurement data from the CSV files in the data directory,
    works out the mean for each day, and then graphs the standard deviation
    of these means.
    """

    data = data_source.load_catchment_data()
    return compute_standard_deviation_by_day_map(data)