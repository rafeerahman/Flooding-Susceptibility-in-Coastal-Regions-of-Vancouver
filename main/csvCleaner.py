import csv
from typing import Dict, List

# read_csv_data('pacificocean_sea_level.csv')


def read_csv_data(filepath: str) -> Dict[str, List]:
    """ Reads the csv data for the average vancouver sea level from 1992 to 2020.
        Filter "NA" values which were set to ''.
        Returns a dictionary with the keys year and sea level, where year corresponds to the list of years,
        and sea level corresponds to a list of sea level data in mm for each year in the list.
    """
    with open(filepath) as file:
        reader = csv.reader(file)

        for _ in range(0, 6):
            next(reader)

        data_sea_level = {'topex_pos': [], 'jason-1': [], 'jason-2': [], 'jason-3': []}

        for row in reader:
            if row[1] != '':
                data_sea_level['topex_pos'].append({row[0]: float(row[1])})
            if row[2] != '':
                data_sea_level['jason-1'].append({row[0]: float(row[2])})
            if row[3] != '':
                data_sea_level['jason-2'].append({row[0]: float(row[3])})
            if row[4] != '':
                data_sea_level['jason-3'].append({row[0]: float(row[4])})

    return data_sea_level
