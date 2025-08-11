from dash import html, dcc, dash_table
from app.figures import *
from app.themes import RED_LINE

min_year = int(df_teams["Year"].min())
max_year = int(df_teams["Year"].max())

years = sorted(df_teams["Year"].unique())
default_year = int(min(years))

# Layout for Gini Logo plot
logo_scatter_section = html.Div(
    [
        html.H3("League Wide Gini vs ROW by Year"),
        html.Div(
            [
                html.Div(
                    dcc.Dropdown(
                        id="logo-year-dropdown",
                        options=get_year_options(),
                        value=default_year,
                        clearable=False,
                        className="dash-dropdown",
                    ),
                    style={"maxWidth": "220px", "marginBottom": "10px"},
                ),
                dcc.Graph(
                    id="logo-scatter-graph",
                    className="full-width",
                    style={"height": "520px"},
                    figure=gini_vs_row_by_year(default_year),
                ),
            ],
            className="plot-container",
        ),
    ]
)

layout = html.Div(
    [
        # Title
        html.H1("Modeling the Impact of Salary Distribution on NHL Team Success"),
        # Sub-heading and callout box
        html.Div(
            [
                html.H3("Interactive Visualizations & Simulations Based On:"),
                html.Div(
                    [
                        dcc.Markdown(
                            """
>**"Modeling the Impact of Salary Distribution on NHL Team Success"**
>*Sloane Holtby, McGill University*
>July 2025
""",
                            style={"whiteSpace": "pre-line"},
                        )
                    ],
                    className="cta-box",
                ),
            ],
            style={"maxWidth": "750px", "paddingLeft": "20px", "textAlign": "left"},
        ),
        # Key Metrics Cards
        html.Div(
            [
                html.Div(
                    [
                        html.Div("Optimal Gini: 0.408", className="card-title"),
                        html.Div(
                            "Performance-maximizing salary dispersion.",
                            className="positive",
                        ),
                    ],
                    className="card",
                ),
                html.Div(
                    [
                        html.Div("Average Salary: $2.17M", className="card-title"),
                        html.Div("Based on 2024-25 league AAVs", className="positive"),
                    ],
                    className="card",
                ),
            ],
            style={"display": "flex", "gap": "20px"},
        ),
        # Overview block
        html.Div(
            [
                html.H2("Overview"),
                html.Div(
                    dcc.Markdown(
                        """
This dashboard explores how NHL teams can optimize performance through strategic salary distribution. Drawing on ten seasons of data and leveraging Gini coefficients to measure intra-team inequality, the analysis reveals a concave relationship between salary dispersion and team success--suggesting that teams perform best when balancing high-paid stars with cost-effective depth players. Using both a Poisson Generalized Linear Model and a dynamic panel Generalized Method of Moments Model, the study identifies an optimal Gini coefficient of ~0.408, providing a practical benchmark for front offices aiming to maximize Regulation + Overtime Wins under the NHL's strict salary cap. Use this app to explore team-by-team salary structures, simulate roster scenarios, and examine how inequality has shaped historical performance.
"""
                    ),
                    className="text-container",
                ),
            ]
        ),
        # League-wide plot
        logo_scatter_section,
        RED_LINE,
        html.H2("Team Explorer"),
        # Team Explorer / Team Salary
        html.Div(
            [
                html.H3("Team Salary", style={"marginTop": "30px"}),
                # Controls row
                html.Div(
                    [
                        # Team dropdown
                        html.Div(
                            dcc.Dropdown(
                                id="ts-team",
                                options=get_team_options(),
                                value=(
                                    get_team_options()[0]["value"]
                                    if get_team_options()
                                    else None
                                ),
                                placeholder="Team Selection",
                                clearable=False,
                                className="dash-dropdown",
                            ),
                            style={"minWidth": "220px"},
                        ),
                        # Year dropdown
                        html.Div(
                            dcc.Dropdown(
                                id="ts-year",
                                options=get_year_options(),
                                value=default_year,
                                placeholder="Year Selection",
                                clearable=False,
                                className="dash-dropdown",
                            ),
                            style={"minWidth": "140px", "marginLeft": "10px"},
                        ),
                        # Info box
                        html.Div(
                            [
                                html.Div(
                                    id="ts-info-line", style={"fontWeight": "bold"}
                                ),
                                html.Div(
                                    id="ts-roster-line", style={"marginTop": "6px"}
                                ),
                            ],
                            className="cta-box",
                            style={
                                "marginLeft": "16px",
                                "padding": "10px 14px",
                                "maxWidth": "500px",
                                "minWidth": "400px",
                                "display": "flex",
                                "flexDirection": "column",
                                "justifyContent": "center",
                                "alignSelf": "center",  # fixed typo
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "gap": "18px",
                        "marginBottom": "10px",
                    },
                ),
                # Plot
                html.Div(
                    dcc.Graph(id="ts-graph", style={"height": "520px"}),
                    className="plot-container",
                ),
            ]
        ),
        # Gini vs ROW
        html.Div(
            [
                html.H3(
                    "Gini vs Regulation + Overtime Wins", style={"marginTop": "30px"}
                ),
                #  Dropdown & Slider
                html.Div(
                    [
                        # Team dropdown
                        html.Div(
                            dcc.Dropdown(
                                id="trend-team",
                                options=get_team_options(),
                                value=(
                                    get_team_options()[0]["value"]
                                    if get_team_options()
                                    else None
                                ),
                                clearable=False,
                                className="dash-dropdown",
                            ),
                            style={"minWidth": "320px"},
                        ),
                        # Year slider
                        html.Div(
                            dcc.RangeSlider(
                                id="trend-years",
                                min=2015,
                                max=2024,
                                step=1,
                                value=[2015, 2024],
                                marks={y: str(y) for y in range(2015, 2025)},
                                tooltip={
                                    "placement": "bottom",
                                    "always_visible": False,
                                },
                            ),
                            style={"flex": "1", "paddingLeft": "14px"},
                        ),
                    ],
                    style={"display": "flex", "alignItems": "center", "gap": "12px"},
                    className="text-container",
                ),
                # Two plots side by side
                html.Div(
                    [
                        html.Div(
                            dcc.Graph(
                                id="row-trend-graph",
                                style={"height": "520px", "width": "100%"},
                                config={"responsive": True},
                            ),
                            style={"flex": 1, "minWidth": 0},
                        ),
                        html.Div(
                            dcc.Graph(
                                id="gini-trend-graph",
                                style={"height": "520px", "width": "100%"},
                                config={"responsive": True},
                            ),
                            style={"flex": 1, "minWidth": 0},
                        ),
                    ],
                    className="plot-container",
                    style={
                        "display": "flex",
                        "gap": "16px",
                        "maxWidth": "1100px",
                        "margin": "0 auto",
                        "width": "100%",
                    },
                ),
            ]
        ),
        # Divider
        RED_LINE,
        html.H2("Model Analysis & Comparison"),
        # GLM Model
        html.Div(
            [
                html.H3("GLM Model", style={"marginTop": "30px"}),
                html.Div(
                    [
                        # Text & Table
                        html.Div(
                            [
                                html.Div(
                                    dcc.Markdown(
                                        r"""This Poisson GLM models Regulation + Overtime Wins (ROW) as a function of the Gini coefficient,
its square, and the previous season's ROW. Using a log-link, the model is:

\[\log(\lambda_i) = \beta_0 + \beta_1 Gini_i + \beta_2 Gini_i^2 + \beta_3 ROW_{i-1}\]

The fitted curve in the plot holds \(\mathrm{ROW}_{i-1}\) at its league-average to show the isolated effect of Gini on ROW."""
                                    ),
                                    className="text-container",
                                    style={"marginBottom": "12px"},
                                ),
                                dash_table.DataTable(
                                    id="glm-table",
                                    columns=glm_table_cols(),
                                    data=glm_table_records(),
                                    style_as_list_view=True,
                                    style_table={"overflowX": "auto", "width": "100%"},
                                    style_cell={
                                        "textAlign": "left",
                                        "padding": "6px 8px",
                                        "fontFamily": "Georgia, serif",
                                        "fontSize": "14px",
                                        "border": "none",
                                    },
                                    style_header={
                                        "fontWeight": "bold",
                                        "color": NAVY,
                                        "border": "none",
                                        "backgroundColor": ACCENT,
                                    },
                                ),
                            ],
                            className="plot-container",
                            style={"flex": "1", "minWidth": "0"},
                        ),
                        # Plot
                        html.Div(
                            dcc.Graph(
                                id="glm-plot",
                                figure=glm_curve_fig(),
                                style={"height": "520px", "width": "100%"},
                            ),
                            className="plot-container",
                            style={"flex": "1", "minWidth": "0"},
                        ),
                    ],
                    style={
                        "display": "flex",
                        "gap": "16px",
                        "alignItems": "stretch",
                        "maxWidth": "1100px",
                        "margin": "0 auto",
                        "width": "100%",
                    },
                ),
            ]
        ),
        # GMM Model
        html.Div(
            [
                html.H3("GMM Model", style={"marginTop": "30px"}),
                html.Div(
                    [
                        # Text & Table
                        html.Div(
                            [
                                html.Div(
                                    dcc.Markdown(
                                        "**Text describing the GMM model**  \n"
                                        "This Poisson GMM models ROW as a function of a quadratic in Gini "
                                        "and lagged ROW. The fitted curve uses the league-average lagged ROW."
                                    ),
                                    className="text-container",
                                    style={"marginBottom": "12px"},
                                ),
                                dash_table.DataTable(
                                    id="gmm-table",
                                    columns=gmm_table_cols(),
                                    data=gmm_table_records(),
                                    style_as_list_view=True,
                                    style_table={"overflowX": "auto", "width": "100%"},
                                    style_cell={
                                        "textAlign": "left",
                                        "padding": "6px 8px",
                                        "fontFamily": "Georgia, serif",
                                        "fontSize": "14px",
                                        "border": "none",
                                    },
                                    style_header={
                                        "fontWeight": "bold",
                                        "color": NAVY,
                                        "border": "none",
                                        "backgroundColor": ACCENT,
                                    },
                                ),
                            ],
                            className="plot-container",
                            style={"flex": "1", "minWidth": "0"},
                        ),
                    ],
                    style={
                        "display": "flex",
                        "gap": "16px",
                        "alignItems": "stretch",
                        "maxWidth": "1100px",
                        "margin": "0 auto",
                        "width": "100%",
                    },
                ),
            ]
        ),
        # Placeholder for Model Comparisons
        html.Div(
            [
                html.H3(" GLM vs GMM", style={"marginTop": "30px"}),
                html.Div(
                    "<!-- Placeholder for comparison plot and table -->",
                    className="plot-container",
                ),
            ]
        ),
        RED_LINE,
        # Footer
        html.Footer(
            [
                html.P("Sloane Holtby | McGill University"),
                html.P(
                    "Based on research using Poisson GLM and GMM models on NHL salary data."
                ),
            ],
            style={
                "marginTop": "40px",
                "textAlign": "center",
                "fontSize": "0.9rem",
                "color": "#1A202C",
            },
        ),
    ],
    className="page-container",
)
