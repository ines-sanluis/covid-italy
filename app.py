# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from colours import *
from map import *
from data_getter import *
from children_creator import *
from vaccines import *

# Load latest data
dfRegional = getRegionalData("latest")
currentDate = dfRegional.loc[0, "data"]
dfNational = getNationalData("latest")
dfRegional, dfNational = addVaccinesData(dfRegional, dfNational)
# Load data of the day before latest
italyFig = getMapFigure()


dropdownOptions = [
    {'label':'Totale', 'value':'total'},
    {'label':'Abruzzo', 'value':13},
    {'label':'Basilicata', 'value':17},
    {'label':'Calabria', 'value':18},
    {'label':'Campania', 'value':15},
    {'label':'Emilia Romagna', 'value':8},
    {'label':'Friuli-Venezia Giulia', 'value':6},
    {'label':'Lazio', 'value':12},
    {'label':'Liguria', 'value':7},
    {'label':'Lombardia', 'value':3},
    {'label':'Marche', 'value':11},
    {'label':'Molise', 'value':14},
    {'label':'P.A. Bolzano', 'value':21},
    {'label':'P.A. Trento', 'value':22},
    {'label':'Piemonte', 'value':1},
    {'label':'Puglia', 'value':16},
    {'label':'Sardegna', 'value':20},
    {'label':'Toscana', 'value':9},
    {'label':'Umbria', 'value':10},
    {'label':"Val d'Aosta", 'value':2},
    {'label':'Veneto', 'value':5},
]

external_stylesheets = [ 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css' ]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(style={"color":"white"}, children=[
    html.Div(
        className="jumbotron text-center bg-dark",
        children =  [
            html.H1("🦠"),
            html.H1("Andamento covid 19"),
            html.P("Data ultimo aggiornamento: "+currentDate.strftime("%d/%m/%Y"))
        ]
    ),
    html.Div(
        className = "col-7 float-right",
        children = [
            html.Div(
                className = "row",
                children = [
                    dcc.Dropdown(
                        id ='demo-dropdown',
                        style = {"width":" 150px !important"},
                        options = dropdownOptions,
                        value='total',
                        searchable = False,
                        clearable = False
                    )
                ]
            ),
            html.Div(id="total-number", className="mt-5"),
            html.Div(id="positives-number",className="mt-5"),
            html.Div(id="vaccines-number",className="mt-5")
        ]
    ),
    html.Div(
        className = "div float-left",
        children = [
            html.Div([ dcc.Graph(figure=italyFig, config={'displayModeBar': False}) ])
        ]
    )
])


@app.callback(
    dash.dependencies.Output('positives-number', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output_positives(value):
    if(value == "total"):
        children = getPositiveChildren(dfNational)
    else:
        children = getPositiveChildren(dfRegional, value)
    return children

@app.callback(
    dash.dependencies.Output('total-number', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output_total(value):
    if(value == "total"):
        children = getTotalChildren(dfNational)
    else:
        children = getTotalChildren(dfRegional, value)
    return children

@app.callback(
    dash.dependencies.Output('vaccines-number', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output_total(value):
    if(value == "total"):
        children = getVaccinesChildren(dfNational)
    else:
        children = getVaccinesChildren(dfRegional, value)
    return children

if __name__ == '__main__':
    app.run_server(debug=True)
