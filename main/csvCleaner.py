import csv
from typing import Dict

# read_csv_data('vancouver_sea_level.csv')


def read_csv_data(filepath: str) -> Dict[str, float]:
    """ Reads the csv data for the average vancouver sea level from 1911 to 2019.
        Filter "NA" values which were set to -99999 in the csv.
        Returns a dictionary of the year mapped to the sea level in mm
    """
    with open(filepath) as file:
        reader = csv.reader(file, delimiter=';')

        next(reader)
        data_sea_level = {}

        for row in reader:
            if (row[1]) != '-99999':
                data_sea_level[str(row[0])] = int(row[1])

    return data_sea_level
