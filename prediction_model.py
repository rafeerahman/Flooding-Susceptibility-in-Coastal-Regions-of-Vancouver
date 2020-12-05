"""
Modelling the data with a regression, and displaying a line graph showing the change in sea level rise over the years,
and displaying predicted values for 20 years into the future.
https://www.analyticsvidhya.com/blog/2015/09/build-predictive-model-10-minutes-python/
"""
from typing import Dict, List, Tuple
import pandas as pd
from data_cleaning import read_csv_data
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Create the regular dataset
dataset = read_csv_data("pacificocean_sea_level.csv")


#############################################
# Creating a dataframe with predicted values
#############################################

# we want to somehow predict the sea level values 20 years from now and in the past

##########
# DISPLAY
##########
def display_graph(data: Dict[str, List[Tuple]]) -> go.Figure():
    """Display a graph of the sea level change over the years. NOT a predictive model
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
    # fig = px.line(x=years, y=levels)

    fig.update_layout(title='Sea Level Anomaly in the North Pacific Ocean from (1972 - 2040)',
                      xaxis_title='Year',
                      yaxis_title='Sea Level Anomaly (mm)')

    return fig

# make subplot method which will display the figure with the data predictions