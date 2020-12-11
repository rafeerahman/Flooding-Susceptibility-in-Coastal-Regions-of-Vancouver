"""
Display the map which shows the susceptible flooding regions - includes interactive features

MAP DATA FROM
https://simplemaps.com/data/canada-cities

This file is Copyright (c) 2020 Lorena Buciu, Rafee Rahman, Kevin Yang, Ricky Yi
"""
from typing import Any

import python_ta
from python_ta import contracts
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd


def display_map(data: Any) -> go.Figure():
    """Displays the map of the given data
    """
    # Main point
    fig = px.scatter_mapbox(data, lat='lat', lon='lng',
                            color_discrete_sequence=['fuchsia'], zoom=3)
    # Flood risk points DUMMY VALUES CURRENTLY
    df = pd.read_csv('below_sea_level.csv')

    fig.add_trace(
        px.scatter_mapbox(
            df,
            lat='lat',
            lon='long',
            color_discrete_sequence=['blue'],
            opacity=0.1,
            zoom=3
        ).data[0]
    )
    fig.update_layout(mapbox_style='open-street-map',
                      mapbox={'center': go.layout.mapbox.Center(lat=data['lat'][0],
                                                                lon=data['lng'][0]), 'zoom': 10})
    fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})

    return fig


if __name__ == '__main__':
    python_ta.check_all(config={
        'extra-imports': ['pandas', 'plotly.express',
                          'plotly.graph_objects'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']

    })
    python_ta.contracts.check_all_contracts()
