from dash import html
import dash_bootstrap_components as dbc

home_page = dbc.Container([

    # =========================
    # IMAGE SECTION
    # =========================
    html.Div([
        html.Img(
            src="/assets/image.png",
            style={
                "display": "block",
                "marginTop": "40px",
                "marginLeft": "auto",
                "marginRight": "auto",
                "width": "70%",
                "height": "auto",
                "borderRadius": "12px",
                "boxShadow": "0px 8px 20px rgba(0,0,0,0.2)"
            }
        )
    ]),

    # =========================
    # PROJECT TITLE (UNDER IMAGE)
    # =========================
html.Div(
    html.H1(
        "Telco Customer Churn Prediction",
        style={
            "fontWeight": "bold",
            "fontSize": "52px",
            "color": "white",
            "padding": "10px",
            "borderRadius": "10px",
            "margin": "0"
        }
    ),
    style={
        "display": "flex",
        "justifyContent": "center", 
        "alignItems": "center",
        "textAlign": "center"
    }
),

    html.Hr(),

    # =========================
    # CONTENT SECTION
    # =========================
    html.Div([

        html.P(
            "This project aims to analyze customer behavior in a telecommunications company "
            "and predict customer churn using advanced data science and machine learning techniques. "
            "The workflow begins with comprehensive data cleaning, including handling missing values, "
            "removing duplicates, correcting data types, and resolving inconsistencies across multiple features.",
            style={"fontSize": "20px"}   
        ),

        html.P(
            "Extensive feature engineering was applied to extract meaningful insights from the data. "
            "New features such as Total Services, Average Monthly Spend, Tenure Groups, and customer risk indicators "
            "were created to better capture customer behavior and improve model performance.",
            style={"fontSize": "20px"}
        ),

        html.P(
            "Dimensionality reduction using PCA and customer segmentation via K-Means clustering were performed "
            "to explore hidden patterns within the data. Feature selection techniques such as Mutual Information, "
            "Random Forest importance, ReliefF, and RFE were applied.",
            style={"fontSize": "20px"}
        ),

        html.P(
            "To address class imbalance, SMOTE and undersampling were used. Performance was evaluated using Accuracy, "
            "Precision, Recall, F1 Score, and ROC-AUC.",
            style={"fontSize": "20px"}
        ),

        html.P(
            "The final model was trained using the best feature set and exported for dashboard integration.",
            style={"fontSize": "20px"}
        ),

        html.Br(),

        html.H4("🔍 Key Highlights:"),

        html.Ul([
            html.Li("Data Cleaning & Preprocessing"),
            html.Li("Feature Engineering"),
            html.Li("PCA & Clustering"),
            html.Li("Feature Selection Methods"),
            html.Li("Handling Imbalanced Data"),
            html.Li("Model Training & Evaluation"),
            html.Li("Interactive Dashboard"),
        ]),

        html.Br(),

        html.P(
            "Use the navigation bar (Home, Dashboard, Model & Performance, Prediction) to explore the project.",
            style={"fontWeight": "bold"}
        ),

    ], style={
        "padding": "60px",
        "maxWidth": "900px",
        "margin": "auto"
    })

], fluid=True)