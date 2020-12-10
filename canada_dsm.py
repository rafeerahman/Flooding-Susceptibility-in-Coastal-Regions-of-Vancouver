"""
File for processing DSM elevation data from https://maps.canada.ca/czs/index-en.html.
"""

from typing import List, Tuple
import numpy as np
import csv


def run_file(filepath: str, sea_level_change: float) -> None:
    """
    Processes DSM surface elevation data .asc file and mutates below_sea_level.csv
    with coordinates of areas below sea level after a given sea level change in metres.
    """
    # read the .asc file
    data = read_asc(filepath)

    # create a list of points with elevation and coordinates
    points = assign_cords(filepath, data)

    # check which points are below sea level
    below_sea_level = check_elevation(points, sea_level_change)

    # write the list of points to below_sea_level.csv
    write_to_csv(below_sea_level)


def test() -> None:
    """
    Remove in final version
    """
    file_name = 'vancouver_surface_elevation.asc'
    sea_level_rise = 6.9
    run_file(file_name, sea_level_rise)


def read_asc(filepath: str) -> List[List[float]]:
    """
    Reads DSM elevation data in the .asc format as given by the
    Geospatial Data Extraction tool from https://maps.canada.ca/czs/index-en.html.
    """

    # read the asc file skipping the header
    data = np.loadtxt(filepath, skiprows=6)

    # return the data as a list
    return list(data.tolist())


def assign_cords(filepath: str, data: List[List[float]]) -> List[Tuple[float, float, float]]:
    """
    Returns a list, sorted by elevation, of data points in the
    format of a tuple of (elevation, latitude, longitude)
    """

    # read the asc file header
    info = list(np.loadtxt(filepath, dtype=str, max_rows=6).tolist())
    num_cols = int(info[0][1])
    num_rows = int(info[1][1])
    lat_bottom = float(info[3][1])  # latitude of bottommost coordinate
    long_left = float(info[2][1])   # longitude of leftmost coordinate
    cell_size = float(info[4][1])   # decimal size of each cell
    no_data_value = int(info[5][1])     # value assigned to area with no data
    lat_top = lat_bottom + num_rows * cell_size     # calculated latitude of topmost coordinate

    # accumulates a list of data points with assigned latitude and longitude
    list_so_far = []
    for i in range(0, num_rows):    # iterate from top to bottom
        for j in range(0, num_cols):    # iterate from left to right
            # exclude cells with no data or elevation 0 (bodies of water)
            if data[i][j] != no_data_value and data[i][j] != 0:
                list_so_far.append((data[i][j], lat_top - cell_size * i, long_left + cell_size * j))

    # sort the list of tuples by the first value of the tuple, elevation
    list_so_far.sort()

    return list_so_far


def check_elevation(data: List[Tuple[float, float, float]], sea_level_change: float) -> \
        List[List[float]]:
    """
    Returns points below sea-level given a change in sea level measured in metres
    """
    list_so_far = []
    i = 0
    while data[i][0] < sea_level_change and i < len(data) - 1:
        list_so_far.append([data[i][1], data[i][2]])
        i += 1
    return list_so_far


def clear_csv() -> None:
    """
    Clear the below_sea_level.csv file
    """
    file = open('below_sea_level.csv', 'r+')
    file.truncate(0)
    file.close()


def write_to_csv(coords: List[List[float]]) -> None:
    """
    Write over the below_sea_level.csv file with a new list of coordinates
    """
    clear_csv()

    with open('below_sea_level.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['lat', 'long'])
        writer.writerows(coords)
