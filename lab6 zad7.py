import json
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from urllib.request import urlopen

# Wczytywanie danych
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

df_unemp = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
    dtype={"fips": str}
)

# Inicjalizacja aplikacji Dash
app = Dash(__name__)

app.layout = html.Div([
    html.H3("Mapa bezrobocia w hrabstwach USA"),
    dcc.Graph(id="mapa"),
    html.H4("Histogram stopy bezrobocia"),
    dcc.Graph(id="histogram")
])

@app.callback(
    Output("mapa", "figure"),
    Input("mapa", "clickData")  # tylko po to, by callback się odpalał
)
def rysuj_mape(_):
    fig = px.choropleth_map(
        df_unemp, geojson=counties, locations='fips', color='unemp',
        color_continuous_scale="Viridis",
        range_color=(0, 12),
        map_style="carto-positron",
        zoom=3, center={"lat": 37.0902, "lon": -95.7129},
        opacity=0.5, labels={'unemp': 'Stopa bezrobocia'}
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

@app.callback(
    Output("histogram", "figure"),
    Input("mapa", "clickData")
)
def pokaz_histogram(clickData):
    if clickData is None:
        # domyślnie: histogram ogólny
        fig = px.histogram(df_unemp, x="unemp", nbins=20, title="Rozkład bezrobocia (USA)")
    else:
        fips_clicked = clickData["points"][0]["location"]
        clicked_row = df_unemp[df_unemp["fips"] == fips_clicked]
        clicked_val = clicked_row["unemp"].values[0] if not clicked_row.empty else None

        fig = px.histogram(df_unemp, x="unemp", nbins=20, title="Rozkład bezrobocia (USA)")
        if clicked_val is not None:
            fig.add_vline(x=clicked_val, line_color="red", line_dash="dash", annotation_text="Wybrane hrabstwo")
    return fig

if __name__ == '__main__':
    app.run(debug=True)
