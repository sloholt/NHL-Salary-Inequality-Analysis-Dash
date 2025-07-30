import pandas as pd

team_data = pd.read_csv(
    r"C:\Users\Sloane\OneDrive\Desktop\project\NHL-Salary-Inequality-Analysis\TeamData.csv"
)
teams = pd.read_csv("data\Teams.csv")

team_data.columns, teams.columns
teams.rename(columns={"Team Name ": "Team_Name"}, inplace=True)
merged = pd.merge(
    team_data, teams[["Team", "Year", "Team_Name"]], on=["Team", "Year"], how="left"
)
merged_path = "data/TeamData_Merged.csv"
merged.to_csv(merged_path, index=False)
merged_path
