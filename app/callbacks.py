from dash import Output, Input
from .figures import *

def register_callbacks(app):
     @app.callback(
        Output("graph-content", "figure"),
        Input("team-year-dropdown", "value")
    )
     def update_team_explorer(year):
        if year is not None:
            return gini_vs_row_by_year(year)
        return gini_vs_row_by_year(year)
