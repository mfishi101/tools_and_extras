import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import milkrunreport, tppreport

index_layout = html.Div([
                            html.Div(html.H2('Dashboard Home Page', className='text-white'),
                            className='navbar navbar-expand-lg navbar-dark bg-dark'),,
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    html.Div(id='page-content',)
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return index_layout
    else:
        return '404 page not found'

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)