import numpy as np
import dash
from dash import html, Input, Output, callback,dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/user")

users = np.arange(1, 611)

user_dropdown = dcc.Dropdown(
    id="user-dropdown",
    options=[{"label": f"User {user}", "value": user} for user in users],
    placeholder="Select User",
    value=1,
    style={"width": "200px", "height": "fit-content"},
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
                                html.H3("Select User", style={"color": "#c41e18"}),
                                user_dropdown,
                                dbc.Button(
                                    "Submit",
                                    href="",
                                    id="user-submit-button",
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


@callback(Output("user-submit-button", "href"), Input("user-dropdown", "value"))
def update_href(user):
    return f"/user/results?user_id={user}"
