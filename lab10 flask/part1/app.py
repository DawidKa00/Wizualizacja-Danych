from flask import Flask, render_template
import pandas as pd
import plotly.express as px

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    df = pd.DataFrame({
        "Grupa": ["A", "B", "C"],
        "Wartość": [10, 20, 30]
    })
    fig = px.bar(df, x='Grupa', y='Wartość', title="Wykres")
    graph_html = fig.to_html(full_html=False)
    return render_template('dashboard.html', graph_html=graph_html)


if __name__ == '__main__':
    app.run(debug=True)
