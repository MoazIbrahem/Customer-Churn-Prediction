from dash import html, dcc, Input, Output
import dash
import joblib
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc

# =========================
# Load model + scaler + features
# =========================
model = joblib.load('data/model.pkl')
scaler = joblib.load('data/scaler.pkl')
features = joblib.load('data/features.pkl')

df_clean = pd.read_csv("data/final_dataset_clean.csv")

# =========================
# Feature metadata
# =========================
feature_ui = {}

for col in features:

    if col in df_clean.columns:

        if df_clean[col].dtype == "object" or df_clean[col].nunique() < 10:
            feature_ui[col] = {
                "type": "categorical",
                "options": df_clean[col].dropna().unique().tolist()
            }
        else:
            feature_ui[col] = {
                "type": "numeric",
                "min": float(df_clean[col].min()),
                "max": float(df_clean[col].max()),
                "mean": float(df_clean[col].mean())
            }
    else:
        feature_ui[col] = {
            "type": "numeric",
            "min": 0,
            "max": 100,
            "mean": 1
        }

# =========================
# PAGE LAYOUT
# =========================
prediction_page = dbc.Container([

    html.H2(
        "🔮 Smart Prediction System",
        style={"color": "white", "textAlign": "center"},
        className="mt-4"
    ),

    html.Hr(style={"borderColor": "#444"}),

    # =========================
    # INPUTS
    # =========================
    html.Div([

        html.Div([

            html.Label(
                f,
                style={"color": "white", "fontWeight": "bold"}
            ),

            # categorical
            dcc.Dropdown(
                id=f,
                options=[{"label": str(x), "value": x}
                         for x in feature_ui[f].get("options", [])],
                value=feature_ui[f].get("options", [None])[0],
                clearable=False,
                style={
                    "marginBottom": "15px",
                    "color": "black"
                }
            ) if feature_ui[f]["type"] == "categorical"

            # numeric
            else dcc.Slider(
                id=f,
                min=feature_ui[f]["min"],
                max=feature_ui[f]["max"],
                value=feature_ui[f]["mean"],
                step=.01,

                marks={
                    int(feature_ui[f]["min"]): str(feature_ui[f]["min"]),
                    int(feature_ui[f]["max"]): str(feature_ui[f]["max"])
                },

                tooltip={"placement": "bottom", "always_visible": True},

                updatemode="drag"
            )

        ]) for f in features

    ]),

    html.Br(),

    # =========================
    # BUTTON
    # =========================
    html.Div([

        html.Button(
            "Predict",
            id="btn",
            n_clicks=0,
            style={
                "padding": "10px 25px",
                "fontWeight": "bold",
                "backgroundColor": "#2ecc71",
                "color": "white",
                "border": "none",
                "borderRadius": "8px",
                "cursor": "pointer"
            }
        )

    ], style={"textAlign": "center"}),

    html.Hr(style={"borderColor": "#444"}),

    # =========================
    # OUTPUT
    # =========================
    html.Div(
        id="out",
        style={
            "backgroundColor": "#161b22",
            "padding": "20px",
            "borderRadius": "10px",
            "color": "white"
        }
    )

], fluid=True)

# =========================
# CALLBACK
# =========================
@dash.callback(
    Output("out", "children"),
    Input("btn", "n_clicks"),
    [Input(f, "value") for f in features]
)
def predict(n, *vals):

    if not n:
        return ""

    if None in vals:
        return html.Div("⚠️ Please fill all fields", style={"color": "red"})

    # =========================
    # FIX 1: Keep feature names
    # =========================
    X = pd.DataFrame([vals], columns=features)

    # =========================
    # FIX 2: Encode categorical values
    # =========================
    for col in X.columns:
        if X[col].dtype == "object":
            X[col] = X[col].astype("category").cat.codes

    # =========================
    # Scale
    # =========================
    X_scaled = scaler.transform(X)

    # =========================
    # Prediction
    # =========================
    pred = model.predict(X_scaled)[0]
    prob = model.predict_proba(X_scaled)[0][1]

    label = "🔥 Churn" if pred == 1 else "✅ No Churn"

    # =========================
    # OUTPUT UI
    # =========================
    return html.Div([

        html.H3(
            f"Prediction: {label}",
            style={"color": "#00d4ff", "textAlign": "center"}
        ),

        html.H4(
            f"Probability: {prob:.2f}",
            style={"color": "#58a6ff", "textAlign": "center"}
        ),

        html.Hr(style={"borderColor": "#444"}),

        html.H4("📊 Input Summary", style={"color": "white"}),

        html.Table([
            html.Tr([
                html.Th("Feature", style={"color": "white"}),
                html.Th("Value", style={"color": "white"})
            ])
        ] + [
            html.Tr([
                html.Td(f, style={"color": "#d1d5db"}),
                html.Td(str(v), style={"color": "#d1d5db"})
            ])
            for f, v in zip(features, vals)
        ], style={"width": "100%"})

    ])