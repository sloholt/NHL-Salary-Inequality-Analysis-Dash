# app/figures.py
import pandas as pd
import plotly.express as px
import json
import numpy as np
import plotly.graph_objects as go

df_teams = pd.read_csv("data/Teams.csv")
with open("assets/Team_Logos.json", "r") as f:
    logo_map = json.load(f)
with open("assets/Team_Names.json") as f2:
    TEAM_NAME_MAP = json.load(f2)


def gini_vs_row_by_year(year):
    filtered_df = df_teams[df_teams["Year"] == year]

    fig = px.scatter(
        filtered_df,
        x="Gini",
        y="ROW",
        hover_name="Team",
        labels={"Gini": "Gini Coefficient", "ROW": "Regulation + Overtime Wins"},
    )

    for _, row in filtered_df.iterrows():
        abbr = row["Team"]
        logo_url = logo_map.get(abbr)
        if logo_url:
            logo_url = logo_url.replace(
                "github.com", "raw.githubusercontent.com"
            ).replace("/blob/", "/")
            fig.add_layout_image(
                dict(
                    source=logo_url,
                    x=row["Gini"],
                    y=row["ROW"],
                    xref="x",
                    yref="y",
                    xanchor="center",
                    yanchor="middle",
                    sizex=0.01,
                    sizey=1.5,
                    sizing="contain",
                    opacity=1,
                    layer="above",
                )
            )

    fig.update_traces(marker_opacity=0)
    fig.update_layout(
        title=f"Gini Coefficient vs ROW in {year}",
        plot_bgcolor="#FFFFFF",
        hoverlabel=dict(bgcolor="white", font=dict(size=13)),
        height=711,
        width=885,
        autosize=False,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig


def get_available_years():
    return sorted(df_teams["Year"].unique())


def get_team_options():
    df = pd.read_csv("data/Teams.csv")
    df.columns = df.columns.str.strip()
    teams = df[["Team", "Team Name"]].drop_duplicates().sort_values("Team Name")
    return [
        {"label": name, "value": abbr}
        for abbr, name in zip(teams["Team"], teams["Team Name"])
    ]


def get_year_options():
    df = pd.read_csv("data/Teams.csv")
    years = sorted(df["Year"].unique())
    return [{"label": str(year), "value": year} for year in years]


def salary_histogram(team, year):
    df = pd.read_csv("data/SalaryData.csv")
    filtered = df[(df["Team"] == team) & (df["Year"] == year)]
    full_team_name = TEAM_NAME_MAP.get(team, team)
    fig = px.bar(
        filtered, x="Player", y="Cap Hit", title=f"{full_team_name} Salary in {year}"
    )
    return fig


def get_gini_and_roster(team, year):
    df = pd.read_csv("data/Teams.csv")
    filtered = df[(df["Team"] == team) & (df["Year"] == year)]
    gini = filtered["Gini"].iloc[0]
    roster_size = filtered["RosterSize"].iloc[0]
    return gini, roster_size


def team_performance_trends(team, year_range):
    df = pd.read_csv("data/Teams.csv")
    filtered = df[
        (df["Team"] == team)
        & (df["Year"] >= year_range[0])
        & (df["Year"] <= year_range[1])
    ]
    full_team_name = TEAM_NAME_MAP.get(team, team)
    row_fig = px.line(
        filtered,
        x="Year",
        y="ROW",
        title=f"{full_team_name} ROW Over Time",
        markers=True,
    )
    gini_fig = px.line(
        filtered,
        x="Year",
        y="Gini",
        title=f"{full_team_name} Gini Coefficient Over Time",
        markers=True,
    )
    return row_fig, gini_fig


def gini_vs_row_with_glm_curve():
    # GLM Coefficient Data
    glm = pd.read_csv("data/glm_model_results.csv")
    glm = glm.set_index("Term")["Estimate"].to_dict()

    beta0 = glm.get("Intercept", 0)
    beta1 = glm.get("Gini", 0)
    beta2 = glm.get("Gini2", 0)
    beta3 = glm.get("Prev_ROW", 0)
    # Team Data
    df = pd.read_csv("data/Teams.csv")
    df.columns = df.columns.str.strip()
    df = df[
        df["Gini"].notnull() & df["ROW"].notnull() & df["ROW_prev_actual"].notnull()
    ]

    fig = px.scatter(
        df,
        x="Gini",
        y="ROW",
        hover_name="Team Name",
        labels={"Gini": "Gini Coefficient", "ROW": "Regulation + Overtime Wins"},
        title="Gini vs ROW with Fitted GLM Curve",
    )
    gini_range = np.linspace(df["Gini"].min(), df["Gini"].max(), 200)
    row_prev_mean = df["ROW_prev_actual"].mean()

    log_lambda = (
        beta0 + beta1 * gini_range + beta2 * gini_range**2 + beta3 * row_prev_mean
    )
    predicted_row = np.exp(log_lambda)

    fig.add_trace(
        go.Scatter(
            x=gini_range,
            y=predicted_row,
            mode="lines",
            name="Fitted GLM Curve",
            line=dict(color="red", width=2),
        )
    )

    fig.update_layout(
        plot_bgcolor="#fff",
        hoverlabel=dict(bgcolor="white", font_size=12),
        height=600,
        width=900,
    )

    return fig
