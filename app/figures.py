# app/figures.py
import pandas as pd
import plotly.express as px
import json

df_teams = pd.read_csv("data/Teams.csv")
with open("assets/Team_Logos.json", "r") as f:
    logo_map = json.load(f)

def gini_vs_row_by_year(year):
    filtered_df = df_teams[df_teams["Year"] == year]

    fig = px.scatter(
        filtered_df,
        x="Gini",
        y="ROW",
        hover_name="Team",
        labels={"Gini": "Gini Coefficient", "ROW": "Regulation + Overtime Wins"}
    )

    for _, row in filtered_df.iterrows():
        abbr = row["Team"]
        logo_url = logo_map.get(abbr)
        if logo_url:
            logo_url = logo_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
            fig.add_layout_image(dict(
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
                layer="above"
            ))

    fig.update_traces(marker_opacity=0)
    fig.update_layout(
        title=f"Gini Coefficient vs ROW in {year}",
        plot_bgcolor="#FFFFFF",
        hoverlabel=dict(bgcolor="white", font=dict(size=13)),
        height=711,
        width=885,
        autosize=False,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def get_available_years():
    return sorted(df_teams["Year"].unique())