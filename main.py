"""
A Python module called main.py whose main block contains the code necessary for running your entire program. When run, this module should:

Load the necessary files from the datasets.
Perform your computations on the data.
Produce an output (which may or may not be interactive).

RUN THIS FILE TO SEE DASH VISUALIZATION
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from prediction_model import *
from map_visualization import display_map, map
from dash.dependencies import Input, Output

if __name__ == '__main__':

    external_stylesheets = [
        'https://codepen.io/chriddyp/pen/bWLwgP.css',
        {
            'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
            'rel': 'stylesheet',
            'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
            'crossorigin': 'anonymous'
        }
    ]

    app = dash.Dash(__name__,
                    external_stylesheets=external_stylesheets)

    app.layout = html.Div([
        html.Div([
            html.Div([
                dcc.Graph(figure=display_map(map))
            ], className="six columns"),
            html.Div([
                dcc.Graph(figure=display_graph(dataset))
            ], className="six columns"),
            html.Div([
                dcc.Graph(figure=display_annual_mean(condensed))
            ], className="six columns"),
        ])
    ])

    app.run_server(debug=True, use_reloader=False)
