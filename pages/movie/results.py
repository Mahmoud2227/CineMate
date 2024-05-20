import dash
from dash import html, dcc, clientside_callback, Input, Output, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/movie/results")

movie_images = [
    "https://www.w3schools.com/w3images/lights.jpg",
    "https://www.w3schools.com/w3images/nature.jpg",
    "https://www.w3schools.com/w3images/mountains.jpg",
    "https://www.w3schools.com/w3images/forest.jpg",
    "https://www.w3schools.com/w3images/nature.jpg",
    "https://www.w3schools.com/w3images/snow.jpg",
    "https://www.w3schools.com/w3images/paris.jpg",
    "https://www.w3schools.com/w3images/nature.jpg",
    "https://www.w3schools.com/w3images/mountains.jpg",
    "https://www.w3schools.com/w3images/forest.jpg",
    "https://www.w3schools.com/w3images/nature.jpg",
    "https://www.w3schools.com/w3images/snow.jpg",
    "https://www.w3schools.com/w3images/paris.jpg",
    "https://www.w3schools.com/w3images/nature.jpg",
    "https://www.w3schools.com/w3images/mountains.jpg",
]


def pagination_component(images, id_name):
    image_elements = [
        dbc.Card(
            dbc.CardImg(src=img, top=True),
            style={
                "marginRight": "10px",
                "minWidth": "300px",
                "maxHeight": "200px",
                "overflow": "hidden",
            },
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
                        "←",
                        id=f"{id_name}-left-arrow",
                        n_clicks=0,
                        className="arrow",
                        style={"height": "40px", "width": "40px"},
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
                        "→",
                        id=f"{id_name}-right-arrow",
                        n_clicks=0,
                        className="arrow",
                        style={"height": "40px", "width": "40px"},
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
            "marginTop": "100px",
        },
    )


def layout(title=None, **other_unknown_query_strings):
    return html.Div(
        [
            dbc.Row(pagination_component(movie_images, "similar")),
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


clientside_callback(
    """
    function(n_clicks_left, n_clicks_right, prev_left, prev_right) {
        var container = document.getElementById('similar-image-container');
        if (n_clicks_left > prev_left) {
            container.scrollLeft -= 500;
        }
        if (n_clicks_right > prev_right) {
            container.scrollLeft += 500;
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

