"""
Display the map which shows the susceptible flooding regions - includes interactive features
GeoPandas seems useful too
Here we will interpret the data with our own logic/calculations
MAP DATA FROM
https://simplemaps.com/data/canada-cities
"""
import python_ta
from python_ta import contracts
import plotly.express as px
# import geopandas as gpd
import plotly.graph_objects as go  # or plotly.express as px

import pandas as pd
from typing import Any

map = pd.read_csv('canadacities.csv')


def display_map(data: Any) -> go.Figure():
    """Displays the map of the given data
    """
    fig = px.scatter_mapbox(data, lat="lat", lon="lng",
                            color_discrete_sequence=["fuchsia"], zoom=3)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


if __name__ == '__main__':

    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']

    })
    python_ta.contracts.check_all_contracts()
