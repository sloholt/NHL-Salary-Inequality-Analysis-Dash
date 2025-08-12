# app/app.py
from dash import Dash, html, dcc
from app.layout import layout
from app.callbacks import register_callbacks

app = Dash(__name__)

app.title = "NHL Salary Inequality Analysis"
app.layout = layout
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
