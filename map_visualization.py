"""
Display the map which shows the susceptible flooding regions - includes interactive features
Use Dash to do this - GeoPandas seems useful too
Here we will interpret the data with our own logic/calculations
MAP DATA FROM
https://simplemaps.com/data/canada-cities
"""
import plotly.express as px
# import geopandas as gpd
import plotly.graph_objects as go  # or plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from prediction_model import display_graph, dataset

map = pd.read_csv('canadacities.csv')

# fig.add_trace( ... )
# fig.update_layout( ... )
fig = px.scatter_mapbox(map, lat="lat", lon="lng",
                        color_discrete_sequence=["fuchsia"], zoom=3)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig),
    dcc.Graph(figure=display_graph(dataset))

])

app.run_server(debug=True, use_reloader=False)
