from dash import Output, Input
from .figures import *
import json

with open("assets/Team_Names.json") as f2:
    TEAM_NAME_MAP = json.load(f2)


def register_callbacks(app):
    @app.callback(
        Output("graph-content", "figure"), Input("team-year-dropdown", "value")
    )
    def update_team_explorer(year):
        if year is not None:
            return gini_vs_row_by_year(year)
        return gini_vs_row_by_year(year)

    @app.callback(
        Output("salary-histogram", "figure"),
        Output("gini-output", "children"),
        Output("roster-output", "children"),
        Input("team-dropdown", "value"),
        Input("year-dropdown", "value"),
    )
    def update_team_explorer(team, year):
        if team is None or year is None:
            return {}, "", ""
        fig = salary_histogram(team, year)
        gini, roster = get_gini_and_roster(team, year)
        full_team_name = TEAM_NAME_MAP.get(team, team)
        gini_text = f"{full_team_name} — Gini Coefficient: {gini:.3f}"
        roster_text = f"Roster Size: {roster} players"
        return fig, gini_text, roster_text

    @app.callback(
        [Output("row-plot", "figure"), Output("gini-plot", "figure")],
        [Input("team-trend-dropdown", "value"), Input("year-slider", "value")],
    )
    def update_trend_graphs(team, year_range):
        return team_performance_trends(team, year_range)
