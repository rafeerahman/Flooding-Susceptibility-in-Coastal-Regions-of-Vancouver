"""
Modelling the data with a regression,
displaying a line graph showing the change in sea level rise over the years,
and displaying predicted values for 20 years into the future.

This file is Copyright (c) 2020 Lorena Buciu, Rafee Rahman, Kevin Yang, Ricky Yi
"""
from typing import List, Tuple, Dict

import python_ta
from python_ta import contracts

import numpy as np
import plotly.express as px
import plotly.graph_objects as go


##########
# DISPLAY
##########
def display_graph(data: Dict[str, List[Tuple]]) -> go.Figure():
    """Return a graph of the sea level change over the years.
    NOT a predictive model
    """
    years = []
    levels = []
    for row in data:
        years.append([pair[0] for pair in data[row]])
        levels.append([pair[1] for pair in data[row]])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years[0], y=levels[0], name='TOPEX'))
    fig.add_trace(go.Scatter(x=years[1], y=levels[1], name='Jason-1'))
    fig.add_trace(go.Scatter(x=years[2], y=levels[2], name='Jason-2'))
    fig.add_trace(go.Scatter(x=years[3], y=levels[3], name='Jason-3'))

    fig.update_layout(title='Sea Level Anomaly in the North Pacific Ocean from (1972 - 2020)',
                      xaxis_title='Year',
                      yaxis_title='Change in Sea Level (mm)')

    return fig


def display_annual_mean(data: Dict[str, List[Tuple]]) -> go.Figure():
    """Return a graph of the sea level change over the years. NOT a predictive model
    """
    years = []
    levels = []
    for row in data:
        years.append([pair[0] for pair in data[row]])
        levels.append([pair[1] for pair in data[row]])

    years = np.concatenate(years)
    levels = np.concatenate(levels)

    fig = px.scatter(x=years, y=levels, trendline="ols")

    fig.update_layout(title='Mean Sea Level Anomaly in the North Pacific Ocean from (1972 - 2020)',
                      xaxis_title='Year',
                      yaxis_title='Change in Sea Level (mm)')

    return fig


def graph_estimations(data: Dict[str, List[Tuple]]) -> go.Figure():
    """Return a graph modelled to display 20 year predictions
    """


if __name__ == '__main__':
    python_ta.check_all(config={
        'extra-imports': ['numpy', 'plotly.express',
                          'plotly.graph_objects'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']

    })
    python_ta.contracts.check_all_contracts()
