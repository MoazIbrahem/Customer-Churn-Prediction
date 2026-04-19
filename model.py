from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# =========================
# Load saved results
# =========================
cm = pd.read_csv("data/confusion_matrix.csv", index_col=0)
roc = pd.read_csv("data/roc_curve.csv")
report = pd.read_csv("data/classification_report.csv")
rf_imp = pd.read_csv("data/rf_importance.csv")

# =========================
# Confusion Matrix (FIXED TEXT)
# =========================
fig_cm = px.imshow(
    cm.values,
    labels=dict(x="Predicted", y="Actual"),
    x=cm.columns,
    y=cm.index,
    title="Confusion Matrix",
    color_continuous_scale="Cividis",
    text_auto = True   
)

fig_cm.update_traces(
    texttemplate="%{z}",
    textfont={"color": "white", "size": 16}
)

fig_cm.update_layout(
    paper_bgcolor="#161b22",
    plot_bgcolor="#161b22",
    font_color="white"
)

# =========================
# ROC Curve
# =========================
fig_roc = px.line(roc, x="FPR", y="TPR", title="ROC Curve")

fig_roc.update_layout(
    paper_bgcolor="#161b22",
    plot_bgcolor="#161b22",
    font_color="white"
)

# =========================
# Feature Importance
# =========================
fig_rf = px.bar(
    rf_imp.head(10),
    x="Importance",
    y="Feature",
    orientation="h",
    title="Top 10 Features (Random Forest)",
    color_discrete_sequence=["#00d4ff"]
)

fig_rf.update_layout(
    paper_bgcolor="#161b22",
    plot_bgcolor="#161b22",
    font_color="white"
)

# =========================
# Classification Report Table
# =========================
if "Unnamed: 0" in report.columns:
    report = report.rename(columns={"Unnamed: 0": "Class"})
report_table = dbc.Table.from_dataframe(
    report.round(3),
    striped=True,
    bordered=True,
    hover=True,
    responsive=True,
    color="dark"
)

# =========================
# MODEL PAGE
# =========================
model_page = dbc.Container([

    html.H2(
        "🤖 Model & Performance",
        className="mt-4",
        style={"color": "white", "textAlign": "center"}
    ),

    html.Hr(),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_cm), md=6),
        dbc.Col(dcc.Graph(figure=fig_roc), md=6),
    ]),

    html.Hr(),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_rf), md=12),
    ]),

    html.Hr(),

    html.H4(
        "Classification Report",
        style={"color": "white", "textAlign": "center"}
    ),

    html.Div(
        report_table,
        style={
            "backgroundColor": "#161b22",
            "padding": "15px",
            "borderRadius": "10px",
            "overflowX": "auto"
        }
    )

], fluid=True)