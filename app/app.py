# app/app.py
from dash import Dash
from .layout import layout

app = Dash(__name__, suppress_callback_exceptions=True)
app.title = "Modeling the Impact of Salary Distribution on NHL Team Success"
app.layout = layout
server = app.server  

from .callbacks import register_callbacks
register_callbacks(app)

