"""
File for data manipulations: cleaning, creating training and testing datasets
"""
import python_ta
from python_ta import contracts

import csv
from typing import Dict, List, Tuple
import sklearn
from sklearn import model_selection
import random


# read_csv_data('pacificocean_sea_level.csv')

def read_csv_data(filepath: str) -> Dict[str, List[Tuple[str, float]]]:
    """ Reads the csv data for the average vancouver sea level from 1992 to 2020.
        Filter "NA" values which were set to ''.
        Returns a dictionary with the keys year and sea level,
        where year corresponds to the list of years,
        and sea level corresponds to a list of sea level data in mm for each year in the list.
    """
    with open(filepath) as file:
        reader = csv.reader(file)

        for _ in range(0, 6):
            next(reader)

        data_sea_level = {'topex_pos': [], 'jason-1': [], 'jason-2': [], 'jason-3': []}

        for row in reader:
            if row[1] != '':
                data_sea_level['topex_pos'].append((row[0], float(row[1])))
            if row[2] != '':
                data_sea_level['jason-1'].append((row[0], float(row[2])))
            if row[3] != '':
                data_sea_level['jason-2'].append((row[0], float(row[3])))
            if row[4] != '':
                data_sea_level['jason-3'].append((row[0], float(row[4])))

    return data_sea_level


# CONDENSED DATA
# get the annual sea level means into a new dataset
def group_means(data: Dict[str, List[Tuple[str, float]]]) -> Dict[str, List[Tuple[str, float]]]:
    """Return a new dataset with the annual means grouped
    """
    new_data = {'topex_pos': [], 'jason-1': [], 'jason-2': [], 'jason-3': []}

    for satellite in data:
        years = {pair[0][0:4] for pair in data[satellite]}

        for year in years:
            annual_mean = 0
            count = 0
            for pair in data[satellite]:
                if year == pair[0][0:4]:
                    annual_mean += pair[1]
                    count += 1
            annual_mean /= count
            new_data[satellite].append((year, annual_mean))

    return new_data

if __name__ == '__main__':
    # python_ta.check_all(config={
    #     'extra-imports': [],  # the names (strs) of imported modules
    #     'allowed-io': [],  # the names (strs) of functions that call print/open/input
    #     'max-line-length': 100,
    #     'disable': ['R1705', 'C0200']
    #
    # })
    python_ta.contracts.check_all_contracts()
