import pandas as pd
import dash
from dash import html, dcc, clientside_callback, Input, Output, State
import dash_bootstrap_components as dbc
from utils.get_top_similar import get_top_similar

dash.register_page(__name__, path="/movie/results")

df_ratings = pd.read_csv("ml-latest-small/ratings.csv")
df_movies = pd.read_csv("ml-latest-small/movies.csv")

df_covers = pd.read_csv("ml-latest-small/movie_covers.csv")
df_links = pd.read_csv("ml-latest-small/links.csv")


def pagination_component(images, id_name):
    image_elements = [
        dbc.Card(
            dbc.CardImg(src=img, top=True),
            style={"marginRight": "10px", "minWidth": "200px", "minHeight": "295px"},
        )
        for img in images
    ]
    return html.Div(
        [
            dcc.Store(id=f"{id_name}-store-left-clicks", data=0),
            dcc.Store(id=f"{id_name}-store-right-clicks", data=0),
            html.Div(
                [
                    html.Button(
                        html.I(
                            className="fa-solid fa-arrow-left",
                            style={"color": "#c41e18"},
                        ),
                        id=f"{id_name}-left-arrow",
                        n_clicks=0,
                        className="arrow",
                        style={
                            "height": "40px",
                            "width": "40px",
                            "backgroundColor": "transparent",
                            "border": "none",
                        },
                    ),
                    html.Div(
                        image_elements,
                        id=f"{id_name}-image-container",
                        style={
                            "display": "flex",
                            "flexDirection": "row",
                            "justifyContent": "space-between",
                            "overflow": "hidden",
                            "whiteSpace": "nowrap",
                            "width": "calc(100vw - 200px)",
                            "scrollBehavior": "smooth",
                        },
                    ),
                    html.Button(
                        html.I(
                            className="fa-solid fa-arrow-right",
                            style={"color": "#c41e18"},
                        ),
                        id=f"{id_name}-right-arrow",
                        n_clicks=0,
                        className="arrow",
                        style={
                            "height": "40px",
                            "width": "40px",
                            "backgroundColor": "transparent",
                            "border": "none",
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                },
            ),
        ],
        style={
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "center",
            "backgroundColor": "black",
        },
    )


def layout(title=None, **other_unknown_query_strings):
    movie_id = df_movies[df_movies["title"] == title]["movieId"].values[0]
    movie_imdb_id = df_links[df_links["movieId"] == movie_id]["imdbId"].values[0]
    movie_poster = df_covers[df_covers["MovieID"] == movie_imdb_id]["CoverURL"].values[
        0
    ]

    sim_df = get_top_similar(df_ratings, df_movies, movieid=movie_id, topn=20)
    sim_df = sim_df.merge(df_links, on='movieId')
    sim_df = sim_df.merge(df_covers, right_on='MovieID', left_on='imdbId')
    similar_movie_posters = sim_df["CoverURL"].values
    
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardImg(src=movie_poster, top=True),
                            style={
                                "width": "200px",
                                "height": "295px",
                            },
                        )
                    ),
                    dbc.Col(
                        html.H1(
                            title,
                            style={"color": "#c41e18", "textAlign": "center"},
                        )
                    ),
                ],
                style={"paddingInline": "100px", "marginTop": "50px"},
            ),
            dbc.Row(
                dbc.Button(
                    html.Img(src="/assets/left-arrow.png", style={"width": "50px"}),
                    href="/movie",
                    style={
                        "backgroundColor": "transparent",
                        "border": "none",
                        "textAlign": "left",
                        "width": "fit-content",
                    },
                ),
                style={"marginBlock": "20px", "paddingInline": "60px"},
            ),
            dbc.Row(
                [
                    html.H2(
                        "Similar Movies",
                        style={"color": "#c41e18", "marginLeft": "90px"},
                    ),
                    pagination_component(similar_movie_posters, "similar"),
                ]
            ),
        ],
        style={
            "backgroundColor": "black",
            "minHeight": "100vh",
            "maxWidth": "100vw",
            "overflowX": "hidden",
        },
    )


clientside_callback(
    """
    function(n_clicks_left, n_clicks_right, prev_left, prev_right) {
        var container = document.getElementById('similar-image-container');
        if (n_clicks_left > prev_left) {
            container.scrollLeft -= 1000;
        }
        if (n_clicks_right > prev_right) {
            container.scrollLeft += 1000;
        }
        return [n_clicks_left, n_clicks_right];
    }
    """,
    [
        Output("similar-store-left-clicks", "data"),
        Output("similar-store-right-clicks", "data"),
    ],
    [
        Input("similar-left-arrow", "n_clicks"),
        Input("similar-right-arrow", "n_clicks"),
    ],
    [
        State("similar-store-left-clicks", "data"),
        State("similar-store-right-clicks", "data"),
    ],
)
