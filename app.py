import pandas as pd
from dash import Dash, html, dcc, Input, Output
import altair as alt



# Read in global data
url = 'https://raw.githubusercontent.com/UofTCoders/workshops-dc-py/master/data/processed/world-data-gapminder.csv'
gm = pd.read_csv(url, parse_dates=['year'])
df = gm[gm['year'] == '1962-01-01']
# Setup app and layout/frontend
app = Dash(__name__,  external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server
app.layout = html.Div([
    html.Iframe(
        id='scatter',
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
    dcc.Slider(id='xslider', min=0, max=240),
    dcc.Dropdown(
        id='xcol-widget',
        value='children_per_woman',  # REQUIRED to show the plot on the first page load
        options=[{'label': col, 'value': col} for col in df.columns]),
    
    dcc.Dropdown(
        id='ycol-widget',
        value='child_mortality',  # REQUIRED to show the plot on the first page load
        options=[{'label': col, 'value': col} for col in df.columns])])

# Set up callbacks/backend
@app.callback(
    Output('scatter', 'srcDoc'),
    Input('xcol-widget', 'value'),
    Input('ycol-widget', 'value'))

def plot_altair(xcol,ycol):
    chart = alt.Chart(df).mark_point().encode(
        x=xcol,
        y=ycol,
        tooltip='life_expectancy').interactive()
    return chart.to_html()

# @app.callback(
#     Output('scatter', 'srcDoc'),
#     Input('xslider', 'value'))
# def update_output(xmax):
#     return plot_altair(xmax)

if __name__ == '__main__':
    app.run_server(debug=True)