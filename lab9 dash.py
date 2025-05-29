# Zadanie 1: Przygotowanie danych i podstawowa wizualizacja
# Wygeneruj dane lub użyj dostępnej biblioteki (np. plotly.data).
# Na podstawie tych danych stwórz aplikację Dash z jednym wykresem, który wyświetla:
# gdpPercap (na osi Y) dla wybranych kontynentów (np. Azja, Ameryka)
# Elementy dodatkowe:
# • dcc.Dropdown do wyboru kontynentu
# • dcc.Graph do wyświetlenia wykresu

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

df = px.data.gapminder()

continents = df['continent'].unique()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Wzrost PKB per capita wg kontynentu"),
    dcc.Dropdown(
        id='continent-dropdown',
        options=[{'label': k, 'value': k} for k in continents],
        value='Asia',
        clearable=False
    ),
    dcc.Graph(id='gdp-plot')
])

@app.callback(
    Output('gdp-plot', 'figure'),
    Input('continent-dropdown', 'value')
)
def update_figure(chosen_continent):
    df_filtered = df[df['continent'] == chosen_continent]
    fig = px.line(df_filtered,
                  x='year',
                  y='gdpPercap',
                  color='country',
                  title=f'PKB per capita w {chosen_continent}')
    return fig


# Uruchom aplikację
if __name__ == '__main__':
    app.run(debug=True)
