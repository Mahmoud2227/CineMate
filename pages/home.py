import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")

layout = html.Div(
    style={
        "backgroundColor": "black",
        "height": "100vh",
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
        "background": "url('/assets/bg-left.png') no-repeat, url('/assets/bg-right.png') no-repeat right",
        "backgroundSize": "contain",
    },
    children=[
        dbc.Container(
            [
                dbc.Row(
                    dbc.Col(
                        html.H1("Welcome To CineMate", style={"color": "inherit"}),
                        width=12,
                        style={"textAlign": "center", "marginBottom": "100px"},
                    )
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Button(
                                    html.Img(
                                        src="/assets/user-icon.gif",
                                        style={
                                            "width": "300px",
                                            "height": "300px",
                                            "borderRadius": "50%",
                                        },
                                    ),
                                    href="/user",
                                    style={
                                        "border": "none",
                                        "backgroundColor": "transparent",
                                    },
                                ),
                                html.H2("User", style={"color": "inherit"}),
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                dbc.Button(
                                    html.Img(
                                        src="/assets/movie-icon.gif",
                                        style={"width": "300px", "height": "300px"},
                                    ),
                                    href="/movie",
                                    style={
                                        "border": "none",
                                        "backgroundColor": "#252a2b",
                                        "width": "300px",
                                        "height": "300px",
                                        "borderRadius": "50%",
                                    },
                                ),
                                html.H2("Movie", style={"color": "inherit"}),
                            ],
                            width=6,
                        ),
                    ],
                    style={"textAlign": "center"},
                ),
            ],
            style={"color": "#c41e18"}
        )
    ],
)
