import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.FONT_AWESOME],
    use_pages=True,
    suppress_callback_exceptions=True,
)

app.layout = html.Div(dcc.Loading(dash.page_container, color='red'), style={"backgroundColor": "#000"})

if __name__ == "__main__":
    app.run(debug=True)
