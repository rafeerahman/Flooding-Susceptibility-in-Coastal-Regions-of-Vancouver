"""
File for data manipulations: cleaning, creating training and testing datasets

This file is Copyright (c) 2020 Lorena Buciu, Rafee Rahman, Kevin Yang, Ricky Yi
"""
import csv

from typing import Dict, List, Tuple
import python_ta
from python_ta import contracts
from theilsen import process_file


###########
# BASE DATA
###########
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


################
# CONDENSED DATA
################
def group_means(data: Dict[str, List[Tuple[str, float]]]) -> Dict:
    """Return a new dataset with the annual means calculated
    """
    new_data = {}

    for satellite in data:
        years = {pair[0][0:4] for pair in data[satellite]}
        years = sorted(years)

        for year in years:
            annual_mean = 0
            count = 0
            for pair in data[satellite]:
                if year == pair[0][0:4]:
                    annual_mean += pair[1]
                    count += 1
            annual_mean /= count

            if year not in new_data:
                new_data[year] = annual_mean
            else:
                prev = new_data[year]
                new_data[year] = (prev + annual_mean) / 2

    return new_data


# HELPER FUNCTION
def means_to_csv(data: Dict) -> None:
    """Convert the mean values dictionary to a csv file so it can be read by pandas
    """
    with open('data_predictions.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['year', 'mean_sea_level'])
        for year in data:
            writer.writerow([year, data[year]])

    # predict_data()


def remove_dupes(data: Dict[str, List[Tuple[str, float]]]) -> None:
    """For the years that have two means due to different satellites,
    get the mean of the two means.
    """
    ...


##################################################################
# Creating a csv with predicted values - using KNN algorithm
# 20 or 100? years into the future
##################################################################
def predict_data() -> None:
    """Write the predicted data points to data_predictions.csv
    """
    values = process_file()
    with open('data_predictions.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        i = 0
        for year in range(2020, values[0]):
            writer.writerow([year, values[1]])
            i += 1


if __name__ == '__main__':
    python_ta.check_all(config={
        'extra-imports': ['csv', 'typing', 'math', 'theilsen'],  # the names (strs) of imported modules
        'allowed-io': ['means_to_csv',
                       'read_csv_data', 'predict_data'],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']

    })
    python_ta.contracts.check_all_contracts()
