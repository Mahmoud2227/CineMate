import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

layout = html.Div(
    style={
        "backgroundColor": "black",
        "height": "100vh",
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
    },
    children=[
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(dbc.Button("User Page", href="/user", color="primary", style={"margin": "10px"})),
                        dbc.Col(dbc.Button("Item Page", href="/movie", color="secondary", style={"margin": "10px"})),
                    ],
                    style={"textAlign": "center"},
                )
            ]
        )
    ],
)
