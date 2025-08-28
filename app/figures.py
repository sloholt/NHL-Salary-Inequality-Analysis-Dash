import pandas as pd
import plotly.express as px
import json
import numpy as np
import plotly.graph_objects as go
from dash import html, dcc
from app.themes import apply_plot_style
from app.constants import *
from dash import get_asset_url


df_teams = pd.read_csv(r"data/Teams.csv")
df_teams.columns = df_teams.columns.str.strip()
df_teams["Year"] = pd.to_numeric(df_teams["Year"], errors="coerce")


df_teams.columns = df_teams.columns.str.strip()
df_all = df_teams[
    df_teams["Gini"].notnull()
    & df_teams["ROW"].notnull()
    & df_teams["ROW_prev_actual"].notnull()
].copy()
df_salary = pd.read_csv(r"data\SalaryData.csv")
df_glm = pd.read_csv(r"data\glm_model_results.csv")
gmm_df = pd.read_csv(r"data/gmm_model_results.csv")
gmm_df.columns = gmm_df.columns.str.strip()

with open(r"app/assets/Team_Logos.json", "r") as f:
    logo_map = json.load(f)
with open(r"app/assets/Team_Names.json") as f2:
    TEAM_NAME_MAP = json.load(f2)


def get_available_years():
    return sorted(df_teams["Year"].unique())


def get_team_options():
    return [
        {"label": full_name, "value": abbr}
        for abbr, full_name in sorted(TEAM_NAME_MAP.items(), key=lambda x: x[1])
    ]


def get_year_options():
    years = sorted(df_teams["Year"].unique())
    return [{"label": str(int(y)), "value": int(y)} for y in years]


def get_gini(team: str, year: int) -> float:
    row = df_teams[(df_teams["Team"] == team) & (df_teams["Year"] == year)]
    return float(row["Gini"].iloc[0]) if not row.empty else float("nan")


def get_roster_size(team: str, year: int) -> int:
    year = int(year)
    sub = df_salary[(df_salary["Team"] == team) & (df_salary["Year"] == year)]
    if sub.empty:
        return 0
    return int(sub["Player"].nunique(dropna=True))


def gini_vs_row_by_year(year):
    year = int(year)
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
            logo_url = get_asset_url(logo_url)
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

    fig.update_traces(
        marker_opacity=0,
        hovertemplate="<b>%{hovertext}</b><br>Gini=%{x:.3f}<br>ROW=%{y}<extra></extra>",
    )
    fig = apply_plot_style(fig, title=f"Gini Coefficient vs ROW in {year}")
    return fig


from app.constants import NAVY  # adjust import path to your project structure


def salary_histogram(team: str, year: int):
    sub = df_salary[
        (df_salary["Team"] == team) & (df_salary["Year"] == int(year))
    ].copy()

    if sub.empty:
        fig = px.bar(title=f"No player salary data for {team} in {year}")
        fig.update_layout(height=520, margin=dict(l=20, r=20, t=50, b=20))
        return fig

    sub["Cap Hit"] = (
        sub["Cap Hit"].astype(str).str.replace(r"[^0-9.]", "", regex=True).astype(float)
    )
    sub = (
        sub.groupby(["Player", "Team", "Year"], as_index=False)
        .agg({"Cap Hit": "max"})
        .sort_values("Cap Hit", ascending=False)
    )

    team_total = sub["Cap Hit"].sum()
    sub["Cap Hit (USD)"] = sub["Cap Hit"].map(lambda x: f"${x:,.0f}")
    sub["% of Team Total"] = (sub["Cap Hit"] / team_total * 100).round(2)

    fig = px.bar(
        sub,
        x="Player",
        y="Cap Hit",
        color_discrete_sequence=[NAVY],  # bar color
        hover_data={
            "Player": True,
            "Team": True,
            "Year": True,
            "Cap Hit (USD)": True,
            "% of Team Total": True,
            "Cap Hit": False,
        },
        title=f"{team} Player Salaries — {year}",
    )

    max_salary = sub["Cap Hit"].max()
    fig.update_yaxes(
        range=[0, max_salary * 1.1], tickprefix="$", separatethousands=True
    )
    fig.update_xaxes(tickangle=45, color=NAVY)
    fig.update_yaxes(color=NAVY)

    fig.update_layout(
        font=dict(color=NAVY),
        barmode="group",
        yaxis_title="Cap Hit (USD)",
        xaxis_title="Player",
        height=520,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig


def team_salary_selection():
    years = get_available_years()
    default_year = int(max(years))
    team_opts = get_team_options()
    default_team = team_opts[0]["value"] if team_opts else None


def team_trend_figures(team: str, year_range: list):
    start, end = int(year_range[0]), int(year_range[1])
    filtered = (
        df_teams[
            (df_teams["Team"] == team)
            & (df_teams["Year"] >= start)
            & (df_teams["Year"] <= end)
        ]
        .sort_values("Year")
        .copy()
    )
    name = TEAM_NAME_MAP.get(team, team)

    # ROW Over Time
    row_fig = px.line(filtered, x="Year", y="ROW", markers=True)
    row_fig.update_traces(
        mode="lines+markers",
        hovertemplate="Year %{x}<br>ROW %{y}<extra></extra>",
        line=dict(color=NAVY),
        marker=dict(color=NAVY),
    )
    row_fig.update_yaxes(title="ROW")
    row_fig.update_xaxes(dtick=1, title=None)
    row_fig = apply_plot_style(row_fig, title=f"{name} ROW Over Time")

    # Gini Over Time
    gini_fig = px.line(filtered, x="Year", y="Gini", markers=True)
    gini_fig.update_traces(
        mode="lines+markers",
        hovertemplate="Year %{x}<br>Gini %{y:.3f}<extra></extra>",
        line=dict(color=NAVY),
        marker=dict(color=NAVY),
    )
    gini_fig.update_yaxes(title="Gini")
    gini_fig.update_xaxes(dtick=1, title=None)
    gini_fig = apply_plot_style(gini_fig, title=f"{name} Gini Coefficient Over Time")

    return row_fig, gini_fig


def glm_curve_fig():
    glm = df_glm.set_index("Term")["Estimate"].to_dict()
    beta0 = glm.get("Intercept", 0.0)
    beta1 = glm.get("Gini", 0.0)
    beta2 = glm.get("Gini2", 0.0)
    beta3 = glm.get("Prev_ROW", 0.0)

    fig = px.scatter(
        df_all,
        x="Gini",
        y="ROW",
        hover_name="Team",
        labels={"Gini": "Gini Coefficient", "ROW": "Regulation + Overtime Wins"},
    )
    fig.update_traces(marker=dict(size=7, color=NAVY), selector=dict(mode="markers"))

    gini_range = np.linspace(df_all["Gini"].min(), df_all["Gini"].max(), 250)
    row_prev_mean = float(df_all["ROW_prev_actual"].mean())
    log_lambda = (
        beta0 + beta1 * gini_range + beta2 * (gini_range**2) + beta3 * row_prev_mean
    )
    predicted_row = np.exp(log_lambda)
    fig.add_trace(
        go.Scatter(
            x=gini_range,
            y=predicted_row,
            mode="lines",
            name="Fitted GLM Curve",
            line=dict(width=2, color=LIGHT_RED),
            hovertemplate="Gini %{x:.3f}<br>Pred ROW %{y:.1f}<extra></extra>",
        )
    )

    fig.update_traces(marker=dict(size=7), selector=dict(mode="markers"))
    fig.update_yaxes(title="ROW")
    fig.update_xaxes(title="Gini")
    fig = apply_plot_style(
        fig,
        title="Gini vs ROW with Fitted GLM Curve",
    )
    return fig


def glm_table_cols():
    return [{"name": col, "id": col} for col in df_glm.columns]


def glm_table_records():
    return df_glm.to_dict("records")


def gmm_table_cols():
    return [{"name": col, "id": col} for col in gmm_df.columns]


def gmm_table_records():
    return gmm_df.to_dict("records")
