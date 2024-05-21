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
)

layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                movie_dropdown,
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "Submit",
                    href="",
                    id="movie-submit-button",
                    color="success",
                    style={"marginTop": "20px"},
                ),
                width={"size": 2, "offset": 5},
            ),
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "Back to Home",
                    href="/",
                    color="warning",
                    style={"marginTop": "20px"},
                ),
                width={"size": 2, "offset": 5},
            ),
        ),
    ],
    style={
        "backgroundColor": "black",
        "minHeight": "100vh",
        "maxWidth": "100vw",
        "overflowX": "hidden",
    },
)


@callback(
    Output("movie-submit-button", "href"),
    Input("movie-dropdown", "value"),
)
def submit(movie):
    return f"/movie/results?title={movie}"
