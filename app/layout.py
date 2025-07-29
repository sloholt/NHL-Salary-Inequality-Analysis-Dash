# app/layout.py
from dash import html, dcc
from .figures import get_available_years


layout = html.Div([
    html.H1("Modeling the Impact of Salary Distribution on NHL Team Success"),
    html.H3("Interactive Visualizations & Simulations Based On:", style={"marginTop": "20px"}),

    html.Div([
        dcc.Markdown('''
> **"Modeling the Impact of Salary Distribution on NHL Team Success"**  
> *Sloane Holtby, McGill University*  
> July 2025
        ''', style={"fontSize": "1rem"})
    ], style={
        "borderLeft": "4px solid #ccc",
        "paddingLeft": "15px",
        "marginBottom": "30px",
        "backgroundColor": "#f9f9f9"
    }),
    html.H2("Overview"),
    html.P("This dashboard explores how NHL teams can optimize performance through strategic salary distribution. Drawing on ten seasons of data and leveraging Gini coefficients to measure intra-team inequality, the analysis reveals a concave relationship between salary dispersion and team success--suggesting that teams perform best when balancing high-paid starts with cost-effective depth players. Using both a Poisson Generalized Linear Model and a dynamic panel Generalized Method of Moments Model, the study identifies an optimal Gini coefficient of ~0.408, providing a practical benchmark for front offices aiming to maximize Regulation + Overtime Wins under the NHL's strict salary cap. Use this app to explore team-by-team salary structures, simulate roster scenarios, and examine how inequality has shaped historical performance. "),
    
    html.P("Use the dropdown below to explore the Gini coefficients and ROW for teams each season."),

    dcc.Dropdown(
        id="team-year-dropdown",
        options=[{"label": str(y), "value": y} for y in get_available_years()],
        placeholder="Select a year",
        style={"width": "300px", "marginBottom": "20px"}
    ),
    html.Div([
        dcc.Graph(id='graph-content')
    ], style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'marginTop': '20px'
    }),
    dcc.Tabs([])  # Your tabs go here
])


