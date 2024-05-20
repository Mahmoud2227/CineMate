import dash
from dash import html, Input, Output, callback, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/movie")

movie_titles = [
    "The Shawshank Redemption",
    "The Godfather",
    "The Dark Knight",
    "The Godfather: Part II",
    "The Lord of the Rings: The Return of the King",
    "Pulp Fiction",
    "Schindler's List",
    "12 Angry",
    "The Lord of the Rings: The Fellowship of the Ring",
    "Fight Club",
    "Forrest Gump",
    "Inception",
    "The Lord of the Rings: The Two Towers",
    "Star Wars: Episode V - The Empire Strikes Back",
    "The Matrix",
]

movie_dropdown = dcc.Dropdown(
    id="movie-dropdown",
    options=[{"label": movie, "value": movie} for movie in movie_titles],
    placeholder="Select Movie",
    value="The Shawshank Redemption",
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
