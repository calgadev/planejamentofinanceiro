import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

import os
import sys
ROOT = os.path.dirname(os.path.dirname(__file__))
SRC = os.path.dirname(__file__)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from app import *
from components import sidebar, extratos, dashboards
from globals import *



# =========  Layout  =========== #
content = html.Div(id="page-content")

app.layout = dbc.Container(children=[
    dcc.Store(id='store-receitas', data=df_receitas.to_dict()),
    dcc.Store(id='store-despesas', data=df_despesas.to_dict()),
    dcc.Store(id='store-cat-receitas', data=df_cat_receitas.to_dict()),
    dcc.Store(id='store-cat-despesas', data=df_cat_despesas.to_dict()),

   dbc.Row([
        dbc.Col([
            dcc.Location(id="url"),
            sidebar.layout
        ], md=2),
        dbc.Col([
            content
        ], md=10)        
   ])

], fluid=True)

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def render_page(pathname):
    if pathname == '/' or pathname == '/dashboard':
        from components import dashboards
        return dashboards.layout
    
    if pathname == '/extratos':
        return extratos.layout
    

if __name__ == "__main__":
    app.run(port=8051, debug=True)
