import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

app = dash.Dash(
    __name__, 
    use_pages=True, 
    external_stylesheets=[dbc.themes.SLATE]
)

# Shared Navigation Bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Analytics Overview", href="/")),
        dbc.NavItem(dbc.NavLink("Analysis", href="/analysis")),
    ],
    brand="Dreaming Devon Portfolio",
    brand_href="/",
    color="primary",
    dark=True,
    className="mb-4"
)

app.layout = html.Div([
    navbar,
    dash.page_container
])

if __name__ == "__main__":
    app.run(debug=True)