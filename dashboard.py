from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# =========================
# Load dataset
# =========================

df1 = pd.read_csv("data/final_dataset.csv")
df2 = pd.read_csv("data/final_dataset_clean.csv")

# =========================
# Churn Distribution
# =========================

fig_churn = px.histogram(df1, x="Churn", color="Churn",
                         title="Churn Distribution",
                         color_discrete_map={"Yes": "tomato", "No": "steelblue"})

fig_churn.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

# =========================
# Average Monthly Charges by Contract & Internet Service
# =========================

pivot = pd.pivot_table(
    df2,
    values="MonthlyCharges",
    index="Contract",
    columns="InternetService",
    aggfunc="mean"
).round(2).reset_index()

fig_avg_charges = px.bar(
    pivot,
    x="Contract",
    y=["DSL", "Fiber optic", "No"],
    title="Average Monthly Charges by Contract & Internet Service",
    barmode="group"
)

# =========================
# Churn Rate by Contract Type
# =========================

churn_rate = df2.groupby("Contract")["Churn"].apply(lambda x: (x == "Yes").mean() * 100).reset_index()
fig_churn_rate = px.bar(churn_rate, x="Contract", y="Churn",
                        title="Churn Rate by Contract Type",
                        labels={"Churn": "Churn %"}, color="Contract")

# =========================
# Total Services vs Churn
# =========================

fig_total_services = px.box(df1, x="Churn", y="TotalServices",
                            title="Total Services vs Churn", color="Churn")

# =========================
# Average Monthly Spend vs Churn
# =========================
fig_avg_spend = px.box(df1, x="Churn", y="AvgMonthlySpend",
                       title="Average Monthly Spend vs Churn", color="Churn")

# =========================
# Tenure Group vs Churn
# =========================

fig_tenure_group = px.histogram(df1, x="TenureGroup", color="Churn",
                                barmode="group", title="Churn by Tenure Group")

# =========================
# Feature Selection Comparison (load summary CSV if saved)
# =========================

try:
    summary = pd.read_csv("data/feature_selection_summary.csv", index_col=0).reset_index()
    summary.rename(columns={"index": "Method"}, inplace=True)

    fig_feature_selection = px.bar(
        summary,
        x="Method",
        y="Accuracy",
        title="Feature Selection Methods Comparison (Accuracy)",
        color="Method"
    )
except Exception as e:
    print(e)
    fig_feature_selection = px.scatter(title="Feature Selection summary not found")

# =========================
# Imbalance Handling Comparison (load balancing summary CSV if saved)
# =========================

try:
    bal_summary = pd.read_csv("data/balancing_summary.csv")
    fig_balancing = px.bar(bal_summary,
                           x=bal_summary.index, y="F1 Score",
                           title="Balancing Impact (F1 Score)",
                           color=bal_summary.index)
except:
    fig_balancing = px.scatter(title="Balancing summary not found")

for fig in [fig_churn, fig_avg_charges, fig_churn_rate,
            fig_total_services, fig_avg_spend, fig_tenure_group,
            fig_feature_selection, fig_balancing]:
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

# =========================
# Dashboard Page Layout
# =========================

dashboard_page = dbc.Container([
    html.H2("📈 Data & Analysis", className="mt-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_churn), md=6),
        dbc.Col(dcc.Graph(figure=fig_avg_charges), md=6),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_churn_rate), md=6),
        dbc.Col(dcc.Graph(figure=fig_total_services), md=6),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_avg_spend), md=6),
        dbc.Col(dcc.Graph(figure=fig_tenure_group), md=6),
    ]),
    html.Hr(),
    html.H3("Feature Selection Comparison"),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_feature_selection), md=12),
    ]),
    html.Hr(),
    html.H3("Imbalance Handling Comparison"),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_balancing), md=12),
    ]),
], fluid=True)
