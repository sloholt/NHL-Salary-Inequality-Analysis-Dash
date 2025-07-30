# app/layout.py
from dash import html, dcc
from app.figures import *
from dash import dash_table

glm_df = pd.read_csv("data/glm_model_results.csv")

layout = html.Div(
    [
        html.H1("Modeling the Impact of Salary Distribution on NHL Team Success"),
        html.H3(
            "Interactive Visualizations & Simulations Based On:",
            style={"marginTop": "20px"},
        ),
        html.Div(
            [
                dcc.Markdown(
                    """
                    > **"Modeling the Impact of Salary Distribution on NHL Team Success"**  
                    > *Sloane Holtby, McGill University*  
                    > July 2025
                    """,
                    style={"fontSize": "1rem"},
                )
            ],
            style={
                "borderLeft": "4px solid #ccc",
                "paddingLeft": "15px",
                "marginBottom": "30px",
                "backgroundColor": "#f9f9f9",
            },
        ),
        html.H2("Overview"),
        html.P(
            "This dashboard explores how NHL teams can optimize performance through strategic salary distribution. Drawing on ten seasons of data and leveraging Gini coefficients to measure intra-team inequality, the analysis reveals a concave relationship between salary dispersion and team success--suggesting that teams perform best when balancing high-paid starts with cost-effective depth players. Using both a Poisson Generalized Linear Model and a dynamic panel Generalized Method of Moments Model, the study identifies an optimal Gini coefficient of ~0.408, providing a practical benchmark for front offices aiming to maximize Regulation + Overtime Wins under the NHL's strict salary cap. Use this app to explore team-by-team salary structures, simulate roster scenarios, and examine how inequality has shaped historical performance. "
        ),
        html.P(
            "Use the dropdown below to explore the Gini coefficients and ROW for teams each season."
        ),
        dcc.Dropdown(
            id="team-year-dropdown",
            options=[{"label": str(y), "value": y} for y in get_available_years()],
            placeholder="Select a year",
            style={"width": "300px", "marginBottom": "20px"},
        ),
        html.Div(
            [dcc.Graph(id="graph-content")],
            style={
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center",
                "marginTop": "20px",
            },
        ),
        html.Div(
            [
                html.H2("Team Explorer"),
                html.P(
                    "Explore how individual NHL teams are structured by salary, and how their Gini coefficient and roster depth vary across seasons."
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label("Select Team"),
                                dcc.Dropdown(
                                    id="team-dropdown",
                                    options=get_team_options(),
                                    placeholder="Select a team",
                                    style={"marginBottom": "10px"},
                                ),
                                html.Label("Select Season"),
                                dcc.Dropdown(
                                    id="year-dropdown",
                                    options=get_year_options(),
                                    placeholder="Select a year",
                                ),
                            ],
                            style={
                                "width": "30%",
                                "display": "inline-block",
                                "verticalAlign": "top",
                            },
                        ),
                        html.Div(
                            [
                                html.Div(
                                    id="gini-output",
                                    style={
                                        "marginBottom": "10px",
                                        "fontWeight": "bold",
                                    },
                                ),
                                html.Div(
                                    id="roster-output", style={"marginBottom": "10px"}
                                ),
                                dcc.Graph(id="salary-histogram"),
                            ],
                            style={
                                "width": "68%",
                                "display": "inline-block",
                                "paddingLeft": "2%",
                            },
                        ),
                    ]
                ),
                html.P(
                    "Use the selector and slider to explore how a team's Regulation + Overtime Wins (ROW) and Gini coefficient evolve over time."
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label("Select Team"),
                                dcc.Dropdown(
                                    id="team-trend-dropdown",
                                    options=get_team_options(),
                                    value="ANA",
                                    style={"width": "100%"},
                                ),
                            ],
                            style={"width": "40%", "marginRight": "2%"},
                        ),
                        html.Div(
                            [
                                html.Label("Select Year Range"),
                                dcc.RangeSlider(
                                    id="year-slider",
                                    min=min(get_available_years()),
                                    max=max(get_available_years()),
                                    value=[
                                        min(get_available_years()),
                                        max(get_available_years()),
                                    ],
                                    marks={
                                        str(y): str(y) for y in get_available_years()
                                    },
                                    step=1,
                                    tooltip={
                                        "placement": "bottom",
                                        "always_visible": False,
                                    },
                                ),
                            ],
                            style={"width": "58%"},
                        ),
                    ],
                    style={
                        "display": "flex",
                        "flexDirection": "row",
                        "alignItems": "center",
                        "marginTop": "15px",
                        "marginBottom": "30px",
                    },
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id="row-plot",
                            style={"display": "inline-block", "width": "48%"},
                        ),
                        dcc.Graph(
                            id="gini-plot",
                            style={"display": "inline-block", "width": "48%"},
                        ),
                    ]
                ),
            ]
        ),
        html.H2("GLM Model Fit"),
        html.P(
            "The fitted curve below is based on a Poisson GLM model relating salary inequality to team performance."
        ),
        html.Div(
            [
                dcc.Graph(
                    id="glm-curve",
                    figure=gini_vs_row_with_glm_curve(),
                    style={"width": "60%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        html.H4("Poisson GLM Coefficients"),
                        dash_table.DataTable(
                            data=glm_df.to_dict("records"),
                            columns=[{"name": i, "id": i} for i in glm_df.columns],
                            style_cell={
                                "textAlign": "left",
                                "padding": "5px",
                                "fontSize": "14px",
                                "fontFamily": "Arial",
                            },
                            style_header={
                                "backgroundColor": "#f2f2f2",
                                "fontWeight": "bold",
                            },
                            style_table={"width": "100%", "overflowX": "auto"},
                        ),
                    ],
                    style={
                        "width": "38%",
                        "display": "inline-block",
                        "paddingLeft": "2%",
                    },
                ),
            ],
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "marginTop": "20px",
            },
        ),
    ]
)
