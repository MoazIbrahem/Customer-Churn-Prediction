import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output

# =========================
# Import pages 
# =========================
from home import home_page
from dashboard import dashboard_page
from model import model_page
from prediction import prediction_page

# =========================
# Initialize app
# =========================
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True
)

app.title = "Telco Churn Dashboard"

# =========================
# Navbar
# =========================
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Dashboard", href="/dashboard")),
        dbc.NavItem(dbc.NavLink("Model", href="/model")),
        dbc.NavItem(dbc.NavLink("Prediction", href="/prediction")),
    ],
    brand="📊 Telco Churn Project",
    brand_href="/",
    color="dark",
    dark=True,
)

# =========================
# Layout
# =========================
app.layout = html.Div([
    dcc.Location(id="url"),
    navbar,
    html.Div(id="page-content")
])

# =========================
# ROUTING (Manual)
# =========================
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):

    if pathname == "/" or pathname is None:
        return home_page

    elif pathname == "/dashboard":
        return dashboard_page

    elif pathname == "/model":
        return model_page

    elif pathname == "/prediction":
        return prediction_page

    else:
        return html.H3("404 Page Not Found", style={"textAlign": "center"})

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)