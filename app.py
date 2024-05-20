import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True, suppress_callback_exceptions=True)

app.layout = html.Div(dash.page_container)

if __name__ == "__main__":
    app.run(debug=True)
