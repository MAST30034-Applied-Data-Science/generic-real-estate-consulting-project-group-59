#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dash import Dash, dcc, html, Input, Output
import dash_daq as daq
import plotly.express as px
import pandas as pd
import numpy as np

df = pd.read_csv("data.csv", index_col=0)

weight_cols = df.columns.drop("Mean").tolist()

variables = [
    'education',
    'income',
    'buy',
    'rentprice',
    'professionals',
    'combined',
    'primary',
    'secondary',
    'schools',
    'trains',
    'trams',
    'buses',
    'stations',
    'shops',
    'theaters',
    'parks',
    'entertainments'
]

app = Dash(__name__)
server = app.server

dp_layout = [
    html.Div("Decimal Precision"),
    daq.Slider(
        id='dp',
        value=1, max=5, min=0, size=150,
        marks={'0': '0', '5':'5'}
    ),
    html.Br()
]

topn_layout = [
    html.Div(id='topn-output'),
    daq.Slider(
        id='topn',
        value=10, max=20, min=3, size=150,
        marks={'3':'3','10':'10','20':'20'}
    ),
    html.Br()
]

selection_layout = []
for var in variables:
    selection_layout.append(html.Div(var.capitalize()))
    selection_layout.append(daq.Slider(
        id=var, value=10, max=10, size=150, 
        marks={'0': '0', '5': '5', '10': '10'}
    ))
    selection_layout.append(html.Br())
    
menu_layout = html.Div(dp_layout + topn_layout + selection_layout)

app.layout = html.Div([
    html.H1('Suburb Liveability Attribute Rankings in Top %'),
    html.Div([menu_layout, dcc.Graph(id="graph", style={'width':'90%','height':'90%'})], 
             style={'flex-direction':'row', 'display':'flex', 'width':'100%','height':'90%'})
])

@app.callback(
    Output("graph", "figure"), 
    Input("dp", "value"),
    Input("topn", "value"),
    *tuple(Input(var, "value") for var in variables))
def filter_heatmap(dp, topn, *kwargs):
    drop_cols = np.array(weight_cols)[np.array(kwargs)==0]
    select_cols = np.array(weight_cols)[np.array(kwargs)!=0]
    select_kwargs = np.array(kwargs)[np.array(kwargs)!=0]
    df['Weighted Mean'] = ((df[select_cols] * select_kwargs) / 10).mean(axis=1)
    fig = px.imshow(df.drop(drop_cols, axis=1).nsmallest(topn, 'Weighted Mean').round(dp), 
                    text_auto=True)
    
    return fig

@app.callback(
    Output('topn-output', 'children'),
    Input('topn', 'value')
)
def update_topn(value):
    return f'Top {value} Suburbs'

app.run_server(debug=True)