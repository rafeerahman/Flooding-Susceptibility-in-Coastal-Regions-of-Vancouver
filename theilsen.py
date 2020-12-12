"""
Theil-Sun Regression Calculation for Points
"""

import statistics
import csv
import pandas
from typing import Tuple, List
from scipy.stats import linregress

dataset = pandas.read_csv('data_predictions.csv')


x_data = []
y_data = []
with open('data_predictions.csv', 'rb') as read_obj:
    reader = csv.reader(read_obj, delimiter='|')
    for row in reader:
        x_data.append(int(row[0]))
        y_data.append(float(row[1]))


def linear_regression(x_coords: list, y_coords: list) -> list:
    """
    returns slope, intercept, correlation coefficient, [p value]
    """

    slope, intercept, correlation, pval, error = linregress(x_coords, y_coords)
    return [slope, intercept, correlation]


def theil_sen_linear_model(x_cords: list, y_cords: list) -> Tuple[float, float]:
    """
    Returns the linear equation once a Theil-Sen analysis is performed on the input
    data. The slope of the model is the median of all slopes between each set of data
    points and calculates the y intercept of the model as well.
    """
    list_of_slopes = []
    for x in range(len(x_cords)):
        slope = (y_cords[x+1] - y_cords[x]) / (x_cords[x + 1] - x_cords[x])
        list_of_slopes.append(slope)

    m = statistics.median(list_of_slopes)
    b = y_cords[1] - m * x_cords[1]
    return (m, b)


def projected_values(slope: float, y_int: float, years: int) -> List[float]:
    """
    Returns a list of projected ocean levels based on a Theil-Sen linear model
    """
    final_values = []
    for num in range(2020, years):
        projection = slope * num + y_int
        final_values.append(projection)
    return final_values
