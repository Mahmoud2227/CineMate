import pandas as pd
import dash
from dash import html, dcc, clientside_callback, Input, Output, State
import dash_bootstrap_components as dbc
from tensorflow.keras.models import load_model
from utils.predict_top_n import predict_top_n_with_loaded_model


dash.register_page(__name__, path="/user/results")

loaded_model = load_model("neural_collaborative_filtering_model.h5")

df_covers = pd.read_csv("ml-latest-small/movie_covers.csv")
df_movies = pd.read_csv("./ml-latest-small/movies.csv")
df_ratings = pd.read_csv("ml-latest-small/ratings.csv")
df_tags = pd.read_csv("ml-latest-small/tags.csv")
df_links = pd.read_csv("ml-latest-small/links.csv")

df_merged = pd.merge(df_ratings, df_tags, on=["userId", "movieId"], how="outer")

df_merged["timestamp_x"] = df_merged["timestamp_x"].fillna(df_merged["timestamp_y"])
df_merged["timestamp_y"] = df_merged["timestamp_y"].fillna(df_merged["timestamp_x"])
df_merged = pd.merge(df_merged, df_links, on="movieId", how="outer")
df_merged = df_merged.drop(columns=["timestamp_y"])
df_merged = df_merged.rename(columns={"timestamp_x": "timestamp"})


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
                        html.I(className="fa-solid fa-arrow-left", style={"color": "#c41e18"}),
                        id=f"{id_name}-left-arrow",
                        n_clicks=0,
                        className="arrow",
                        style={"height": "40px", "width": "40px", "backgroundColor": "transparent", "border": "none"},
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
                        html.I(className="fa-solid fa-arrow-right" , style={"color": "#c41e18"}),
                        id=f"{id_name}-right-arrow",
                        n_clicks=0,
                        className="arrow",
                        style={"height": "40px", "width": "40px", "backgroundColor": "transparent", "border": "none"},
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


def layout(user_id, **other_unknown_query_strings):
    sorted_movies_ids = df_merged[df_merged["userId"] == int(user_id)].sort_values(
        "timestamp"
    )["imdbId"]
    recent_movie_posters = df_covers[df_covers["MovieID"].isin(sorted_movies_ids)][
        "CoverURL"
    ]

    recommended_movies_ids = predict_top_n_with_loaded_model(
        loaded_model=loaded_model,
        ratings=df_ratings,
        movies=df_movies,
        user_id=int(user_id),
        n=20,
    )

    imdb_ids = df_links[df_links["movieId"].isin(recommended_movies_ids)]["imdbId"]
    recommended_movies_posters = df_covers[df_covers["MovieID"].isin(imdb_ids)][
        "CoverURL"
    ]

    return html.Div(
        [
            dbc.Row(
                [
                    html.H2(
                        "Recently Watched",
                        style={"color": "#c41e18", "marginLeft": "90px"},
                    ),
                    pagination_component(recent_movie_posters, "recent"),
                ],
                # style={"marginTop": "100px"},
            ),
            dbc.Row(
                dbc.Button(
                    html.Img(src="/assets/left-arrow.png", style={"width": "50px"}),
                    href="/user",
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
                        "Recommended Movies",
                        style={"color": "#c41e18", "marginLeft": "90px"},
                    ),
                    pagination_component(recommended_movies_posters, "recommended"),
                ],
                # style={"marginTop": "60px"},
            ),
        ],
        style={
            "backgroundColor": "black",
            "minHeight": "100vh",
            "maxWidth": "100vw",
            "overflowX": "hidden",
        },
    )

# JavaScript for handling the scroll
clientside_callback(
    """
    function(n_clicks_left, n_clicks_right, prev_left, prev_right) {
        var container = document.getElementById('recent-image-container');
        scrollAmount = container.clientWidth - 100;
        if (n_clicks_left > prev_left) {
            container.scrollLeft -= scrollAmount;
        }
        if (n_clicks_right > prev_right) {
            container.scrollLeft += scrollAmount;
        }
        return [n_clicks_left, n_clicks_right];
    }
    """,
    [
        Output("recent-store-left-clicks", "data"),
        Output("recent-store-right-clicks", "data"),
    ],
    [Input("recent-left-arrow", "n_clicks"), Input("recent-right-arrow", "n_clicks")],
    [
        State("recent-store-left-clicks", "data"),
        State("recent-store-right-clicks", "data"),
    ],
)

clientside_callback(
    """
    function(n_clicks_left, n_clicks_right, prev_left, prev_right) {
        var container = document.getElementById('recommended-image-container');
        scrollAmount = container.clientWidth - 100;
        if (n_clicks_left > prev_left) {
            container.scrollLeft -= scrollAmount;
        }
        if (n_clicks_right > prev_right) {
            container.scrollLeft += scrollAmount;
        }
        return [n_clicks_left, n_clicks_right];
    }
    """,
    [
        Output("recommended-store-left-clicks", "data"),
        Output("recommended-store-right-clicks", "data"),
    ],
    [
        Input("recommended-left-arrow", "n_clicks"),
        Input("recommended-right-arrow", "n_clicks"),
    ],
    [
        State("recommended-store-left-clicks", "data"),
        State("recommended-store-right-clicks", "data"),
    ],
)
