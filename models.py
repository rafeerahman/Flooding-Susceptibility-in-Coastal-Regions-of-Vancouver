"""
Modelling the data with graphs and a map
which shows the susceptible flooding regions - includes interactive features

This file is Copyright (c) 2020 Lorena Buciu, Rafee Rahman, Kevin Yang, Ricky Yi
"""
from typing import List, Tuple, Dict

import python_ta
from python_ta import contracts

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import csv


################
# DISPLAY GRAPHS
################
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

    fig.update_layout(title='Sea Level Anomaly in the North Pacific Ocean from (1992 - 2020)',
                      xaxis_title='Year',
                      yaxis_title='Change in Sea Level (mm)')

    return fig


def display_annual_mean(data: str) -> go.Figure():
    """Return a graph of the sea level change over the years.
    Can work with the prediction model
    """
    df = pd.read_csv(data)

    fig = px.scatter(df, x=df['year'], y=df['mean_sea_level'], trendline="ols")

    fig.update_layout(title='Mean Sea Level Anomaly in the North Pacific Ocean from (1992 - 2300)',
                      xaxis_title='Year',
                      yaxis_title='Average Change in Sea Level (mm)')

    return fig


#############
# DISPLAY MAPS
#############
def display_map() -> go.Figure():
    """Displays the map of the given data
    """
    # Main point - Vancouver latitude and longitude
    fig = px.scatter_mapbox(lat=[49.2500], lon=[-123.1000],
                            color_discrete_sequence=['fuchsia'], zoom=3)

    df = pd.read_csv('below_sea_level.csv')

    fig.add_trace(
        px.scatter_mapbox(
            df,
            title='Map of Vancouver Indicating Flood Regions',
            lat='lat',
            lon='long',
            color="elevation",
            color_discrete_sequence=['blue'],
            opacity=0.1,
            zoom=3
        ).data[0]
    )
    fig.update_layout(mapbox_style='open-street-map',
                      mapbox={'center': go.layout.mapbox.Center(lat=mean_coords()[0],
                                                                lon=mean_coords()[1]), 'zoom': 10})
    fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
    fig.update_coloraxes(colorscale='RdBu')

    return fig


def mean_coords() -> Tuple[float, float]:
    """
    Returns the average latitude and longitude of points contained in below_sea_level.csv
    """
    lat_total = 0
    long_total = 0
    cnt = 0
    with open('below_sea_level.csv') as file:
        reader = csv.reader(file)

        # skip header
        next(reader)

        # accumulate each row
        for row in reader:
            lat_total += float(row[0])
            long_total += float(row[1])
            cnt += 1

    # return the average
    return (lat_total / cnt, long_total/cnt)


if __name__ == '__main__':
    python_ta.check_all(config={
        'extra-imports': ['numpy', 'plotly.express',
                          'plotly.graph_objects', 'pandas'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']

    })
    python_ta.contracts.check_all_contracts()
