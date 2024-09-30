from dash import dcc
from dash import html

def create_dash_layout():
    return html.Div([
        html.H1("Patient Data Dashboard"),
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [{'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'}],
                'layout': {'title': 'Basic Data Visualization'}
            }
        )
    ])
