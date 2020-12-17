from dash.dependencies import Input, Output
from app import app, server
from layoutHome import layoutHome
from layoutFirstPage import layoutFirstPage
from layoutSecondPage import layoutSecondPage

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# CSS
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "19rem",
    "padding": "2rem 1rem",
    "background-color": "#555",
    "color": "#FFF"
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# Navbar
sidebar = dbc.Container(   
         dbc.Col(
             html.Div(
                [
                    html.H2(dbc.Alert("Dashboard", color="warning"), className="text-center"),
                    html.H4("Emotions wheel", className="display-6 text-center"),
                    html.Hr(),
                    html.P(
                        "Dashboard Test v0.1", className="lead"
                    ),
                    html.P(
                        "Navigation"
                         ),
                    dbc.Nav(
                        [
                            dbc.Button("Home", href="/", id="page1-link"),
                            dbc.Button("Datasets", href="/apps/app1", id="page2-link"),
                            dbc.Button("Predicts", href="/apps/app2", id="page3-link"),
                        ],
                        vertical=True,
                        pills=True,
                    ),
                ],
                style=SIDEBAR_STYLE,
            )
        )
     )

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(
    [Output(f"page{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page{i}" for i in range(1, 4)]

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/' :
        return layoutHome
    elif pathname == '/apps/app1':
        return layoutFirstPage
    elif pathname == '/apps/app2':
        return layoutSecondPage
    else:
        #return '404'
        return dbc.Jumbotron([
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
        ])    
    
if __name__ == '__main__':
    app.run_server()
