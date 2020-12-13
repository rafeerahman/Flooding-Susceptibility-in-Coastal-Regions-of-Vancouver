"""
CSC110 Final Project - Predicting the Flooding Susceptibility of the Vancouver region

This is the main module, it will:
    - Load the necessary files from the datasets
    - Perform computations on the data
    - Produce an interactive output

===================================================
Instructions:
-ensure that all of the required modules from requirements.txt
are successfully installed
-download vancouver_surface_elevation.asc, pacificocean_sea_level.csv
RUN THIS FILE TO SEE DASH VISUALIZATION
-click the link in the console output to view the visualizations
===================================================

This file is Copyright (c) 2020 Lorena Buciu, Rafee Rahman, Kevin Yang, Ricky Yi
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from data_cleaning import read_csv_data, group_means, means_to_csv
from models import display_graph, display_annual_mean, display_map
from dash.dependencies import Input, Output
from canada_dsm import run_file

# Create the datasets & Call computing functions
dataset = read_csv_data("pacificocean_sea_level.csv")
# calculate the annual means
condensed = group_means(dataset)
# CREATE data_predictions.csv
means_to_csv(condensed)

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

# OUTPUT
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets)

app.layout = html.Div([

    html.H1("Flooding Susceptibility in Vancouver Coastal Regions"),

    html.Div(
        className="row",
        children=[
            html.Div(
                className="six columns",
                children=[
                    html.Div([
                        dcc.Graph(id='map_plot'),
                        dcc.Slider(
                            id='year_slider',
                            min=2020,
                            max=2300,
                            step=1,
                            marks={year: str(year) for year in range(2020, 2320, 20)}, value=2020,
                        ),
                        dcc.Slider(
                            id='sea_level_slider',
                            min=0,
                            max=100,
                            step=0.001,
                            marks={num: str(num) + 'm' for num in range(0, 110, 10)}, value=0.071
                        ),
                    ])
                ]
            ),
            html.Div(
                className="six columns",
                children=html.Div([
                    dcc.Graph(
                        id='right-top-graph',
                        figure=
                        display_graph(dataset)

                    ),
                    dcc.Graph(
                        id='right-bottom-graph',
                        figure=
                        display_annual_mean('data_predictions.csv')

                    ),

                ])
            )
        ]
    )
], style={'margin-left': '50px', 'margin-right': '50px'})


@app.callback(Output('map_plot', 'figure'),
              Input('year_slider', 'value'),
              Input('sea_level_slider', 'value'))
def update_map(year, sea_level) -> any:
    """
    Updates the map based on the value of the most recently used slider
    """
    ctx = dash.callback_context

    # run on start-up or if year_slider is used
    if ctx.triggered[0]['prop_id'] == '.' or ctx.triggered[0]['prop_id'] == 'year_slider.value':
        # run_file() function will call other computation functions
        df = pd.read_csv('data_predictions.csv')
        row_id = df.index[df['year'] == year].tolist()
        val = df.loc[row_id[0]]['mean_sea_level']
        sea_level = val / 1000  # convert mm to m
        run_file('elevation_data.asc', sea_level)

    # run if sea_level_slider is used
    else:
        run_file('elevation_data.asc', sea_level)
    return display_map()


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
