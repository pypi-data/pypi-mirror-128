import dash
from dash import dcc
from dash import html
from dash.dependencies import Input,Output
import argparse
import webbrowser
from threading import Timer
from PyMacroFin.kolmogorov import stationary_plot
import cloudpickle
import PyMacroFin.utilities as util
import pandas as pd
import dash_daq as daq
from PyMacroFin.grid import grid
from flask import request


app = dash.Dash(__name__,external_scripts=['https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML'])
title_text = "PyMacroFin Model Visualization"
app.layout = html.Div([ html.H1(id='header',
                                className='banner',
                                children=title_text),
                        dcc.Interval(id='header-update',interval=2000,n_intervals=0),
                        html.Div([
                            dcc.Graph(id='fig1',figure={}),
                            dcc.Interval(id='fig1_update',interval=20000,n_intervals=0)
                        ])])
                        
        
@app.callback(Output('fig1','figure'),Input('fig1_update','n_intervals'))
def update_dash1(interval):
    """
    Utility pipe function for updating dash application from the utilities module
    """
    df = pd.read_csv('./tmp{}_stationary/dash_data.csv'.format(name))
    fig = stationary_plot(m,df)
    return fig
    
    
@app.callback(Output('header','children'),Input('header-update','n_intervals'))
def update_dash3(interval):
    """
    Utility pipe function for updating dash application from the utilities module
    """
    return title_text+': {}'.format(name)
        
    
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n','--name',help='set name of model')
    parser.add_argument('-d','--dash_debug')
    parser.add_argument('-p','--port',help='set port')
    args = parser.parse_args()
    
    if args.name:
        name = args.name
    else:
        name = ''
    if args.dash_debug:
        dash_debug = args.dash_debug
    else:
        dash_debug = True
    if args.port:
        myport = args.port
    else:
        myport = 8050

    m = cloudpickle.load(open('./tmp{}_stationary/init.pkl'.format(name),'rb')) 
    m.grid = grid(m.options)
 
    app.run_server(debug=dash_debug,port=myport)
