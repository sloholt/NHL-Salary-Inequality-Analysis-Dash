# app/app.py
from dash import Dash, html, dcc
from app.layout import layout
from app.callbacks import register_callbacks

app = Dash(__name__)

app.index_string = """
<!DOCTYPE html>
<html>
  <head>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
  </head>
  <body>
    {%app_entry%}
    <footer>
      {%config%}{%scripts%}{%renderer%}
    </footer>
  </body>
</html>
"""

app.title = "NHL Salary Inequality Analysis"
app.layout = layout
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
