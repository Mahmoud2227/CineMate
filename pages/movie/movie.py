import pandas as pd

import dash
from dash import html, Input, Output, callback, dcc
import dash_bootstrap_components as dbc

movies = pd.read_csv("ml-latest-small/movies.csv")

dash.register_page(__name__, path="/movie")

movie_titles = movies["title"].unique()

movie_dropdown = dcc.Dropdown(
    id="movie-dropdown",
    options=[{"label": movie, "value": movie} for movie in movie_titles],
    placeholder="Select Movie",
    value=movie_titles[0],
    style={"width": "230px", "height": "fit-content"},
)

layout = dbc.Row(
    [
        dbc.Col(
            dbc.Button(
                html.Img(src="/assets/left-arrow.png", style={"width": "50px"}),
                href="/",
                style={"backgroundColor": "transparent", "border": "none"},
            ),
            width=1,
        ),
        dbc.Col(html.Img(src="/assets/user-bg.png"), width=5),
        dbc.Col(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H3("Select Movie", style={"color": "#c41e18"}),
                                movie_dropdown,
                                dbc.Button(
                                    "Submit",
                                    href="",
                                    id="movie-submit-button",
                                    style={
                                        "backgroundColor": "#c41e18",
                                        "border": "none",
                                    },
                                ),
                            ],
                            # width=3,
                            style={
                                "display": "flex",
                                "alignItems": "center",
                                "justifyContent": "center",
                                "gap": "10px",
                            },
                        ),
                    ],
                    style={
                        "paddingInline": "100px",
                        "marginBlock": "auto",
                    },
                )
            ],
            width=6,
            style={"display": "flex", "flexDirection": "column", "height": "100vh"},
        ),
    ],
    style={
        "backgroundColor": "black",
        "minHeight": "100vh",
        "maxWidth": "100vw",
        "overflowX": "hidden",
        "paddingInline": "50px",
    },
    align="center",
)


@callback(
    Output("movie-submit-button", "href"),
    Input("movie-dropdown", "value"),
)
def submit(movie):
    return f"/movie/results?title={movie}"
