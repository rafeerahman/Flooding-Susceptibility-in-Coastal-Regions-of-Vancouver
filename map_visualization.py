"""
Display the map which shows the susceptible flooding regions - includes interactive features

MAP DATA FROM
https://simplemaps.com/data/canada-cities

This file is Copyright (c) 2020 Lorena Buciu, Rafee Rahman, Kevin Yang, Ricky Yi
"""
import python_ta
from python_ta import contracts
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd


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
                      mapbox={'center': go.layout.mapbox.Center(lat=49.2500,
                                                                lon=-123.1000), 'zoom': 10})
    fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
    fig.update_coloraxes(colorscale='RdBu')

    return fig


if __name__ == '__main__':
    python_ta.check_all(config={
        'extra-imports': ['pandas', 'plotly.express',
                          'plotly.graph_objects'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']

    })
    python_ta.contracts.check_all_contracts()
