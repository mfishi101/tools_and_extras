import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app import app
from config.config import *

layout = html.Div([
    html.Div(html.H2('Dashboard Login', className='text-white'),
                            className='navbar navbar-expand-lg navbar-dark bg-dark'),
    html.H4('Please input your login details', className='p-3'),
    html.Div(dcc.Input(
        id='user-in',
        placeholder='username',
        style={'fontSize':28},
    className='px-3'
    ), className='p-3'),
    html.Div(dcc.Input(
        id='pwd-in',
        placeholder='password',
        style={'fontSize':28},
        type='password',
    className='px-3'), className='p-3'),
    html.Div(html.Button(
        id='submit-credentials',
        n_clicks=0,
        children='Submit',
        style={'fontSize':28},
    ),className='p-3'),
    html.H3(html.Div(id='display-page',className='p-3'))
])

@app.callback(
    Output('display-page', 'children'),
    [Input('submit-credentials', 'n_clicks')],
    [State('user-in', 'value'),
    State('pwd-in', 'value')])
def output(n_clicks, user, pwd):

    if (user == None or pwd == None):
        return 'awaiting credentials'
    # if (users[username] and users[password])
    else:
        return dcc.Location(pathname='/', id='no_id')

    