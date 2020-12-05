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
from prediction_model import display_graph, dataset
from map_visualization import display_map, map


if __name__ == '__main__':

    app = dash.Dash()
    app.layout = html.Div([
        dcc.Graph(figure=display_map(map)),
        dcc.Graph(figure=display_graph(dataset))

    ])

    app.run_server(debug=True, use_reloader=False)
