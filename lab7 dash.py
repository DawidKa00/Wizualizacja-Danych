import numpy as np
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Interaktywny wykres funkcji matematycznych"),

    html.Div([
        html.H4("Funkcja:"),
        dcc.Input(id="function-input", type="text", value="np.sin(x)",
                  style={'width': '80%'}),
    ]),

    html.Div([
        html.H4("Zakres X:"),
        dcc.Input(id="x-range-input", type="text", value='(-10,10)',
                  style={'width': '38%'}),

        html.H4("Zakres Y:"),
        dcc.Input(id="y-range-input", type="text", value='(-1,1)',
                  style={'width': '38%'}),
    ], style={"marginTop": 10}),

    html.Div([
        html.H4("Typ linii:"),
        dcc.Dropdown(
            id='line-style-dropdown',
            options=[
                {'label': 'Linia ciągła', 'value': 'solid'},
                {'label': 'Linia przerwana', 'value': 'dash'},
                {'label': 'Linia kropkowana', 'value': 'dot'},
            ],
            value='solid',
            style={'width': '38%'}
        ),
    ], style={"marginTop": 10}),

    html.Div([
        html.H4("Kolor:"),
        dcc.Dropdown(
            id='color-dropdown',
            options=[
                {'label': 'Czerwony', 'value': 'red'},
                {'label': 'Zielony', 'value': 'green'},
                {'label': 'Fiolet', 'value': 'violet'},
                {'label': 'Niebieski', 'value': 'blue'},
                {'label': 'Żółty', 'value': 'yellow'},
                {'label': 'Czarny', 'value': 'black'},
                {'label': 'Biały', 'value': 'white'},
            ],
            value='blue',
            style={'width': '80%'}
        )
    ], style={"marginTop": 10}),

    html.Button('Zatwierdź', id='submit-button', n_clicks=0, style={"marginTop": 10}),

    dcc.Graph(id="function-graph")
])


@app.callback(
    Output("function-graph", "figure"),
    Input("submit-button", "n_clicks"),
    State("function-input", "value"),
    State("x-range-input", "value"),
    State("y-range-input", "value"),
    State("line-style-dropdown", "value"),
    State("color-dropdown", "value")
)
def update_graph(n_clicks, function_input, x_range, y_range, line_style, color):
    try:
        x_min, x_max = map(float, x_range.strip('()').split(','))
        y_min, y_max = map(float, y_range.strip('()').split(','))
    except ValueError:
        return go.Figure(
            layout=go.Layout(title="Błąd: Nieprawidłowy zakres osi X lub Y")
        )

    x = np.linspace(x_min, x_max, 400)

    try:
        # Safer eval with limited scope
        y = eval(function_input, {"np": np, "__builtins__": {}}, {"x": x})
    except Exception as e:
        return go.Figure(
            layout=go.Layout(title=f"Błąd w funkcji: {e}")
        )

    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines',
                                    line=dict(color=color, dash=line_style)))
    fig.update_layout(
        title=f"Wykres funkcji {function_input}",
        xaxis_title="X",
        yaxis_title="Y",
        xaxis=dict(range=[x_min, x_max]),
        yaxis=dict(range=[y_min, y_max]),
    )
    return fig


if __name__ == '__main__':
    app.run(debug=True)
