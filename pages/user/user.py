import numpy as np
import dash
from dash import html, Input, Output, callback
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/user")

users = np.arange(1, 611)
genres = [
    "Action",
    "Adventure",
    "Comedy",
    "Drama",
    "Horror",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Thriller",
    "Western",
]

user_select = dbc.Select(
    id="user-select",
    options=[{"label": f"User {user}", "value": user} for user in users],
    value=1,
    style={"width": "fit-content", "height": "fit-content"},
)

genres_select = dbc.Select(
    id="genres-select",
    options=[{"label": genre, "value": genre} for genre in genres],
    value="Action",
    style={"width": "fit-content", "height": "fit-content"},
)

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [html.H3("Select User"), user_select],
                    width=6,
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "gap": "10px",
                    },
                ),
                dbc.Col(
                    [html.H3("Select Genre"), genres_select],
                    width=6,
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "gap": "10px",
                    },
                ),
            ],
            style={"paddingTop": "50px", "paddingInline": "100px"},
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "Submit",
                    href="",
                    id="user-submit-button",
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
    Output("user-submit-button", "href"),
    Input("user-select", "value"),
    Input("genres-select", "value"),
)
def update_href(user, genre):
    return f"/user/results?user_id={user}&genre={genre}"
