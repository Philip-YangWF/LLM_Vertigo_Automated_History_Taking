from dash import Dash
from flask import current_app
from .layouts import create_dash_layout

def init_dashboard(server):
    dash_app = Dash(__name__, server=server, url_base_pathname='/dashboard/')
    with server.app_context():
        dash_app.layout = create_dash_layout()
    return dash_app
