from flask import Flask, render_template, request, redirect, url_for, flash, session
import plotly
import plotly.graph_objs as go
import json
import random

app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY='bardzosekretnawartosc',
))

DANE = [
    {
        'pytanie': 'Stolica Hiszpani, to:',
        'odpowiedzi': ['Madryt', 'Warszawa', 'Barcelona'],
        'poprawna': 'Madryt'
    },
    {
        'pytanie': 'Objętość sześcianu o boku 6 cm, wynosi:',
        'odpowiedzi': ['36', '216', '18'],
        'poprawna': '216'
    },
    {
        'pytanie': 'Symbol pierwiastka Helu, to:',
        'odpowiedzi': ['Fe', 'H', 'He'],
        'poprawna': 'He'
    },
    {
        'pytanie': 'Ile wynosi pierwiastek kwadratowy z 16?',
        'odpowiedzi': ['2', '4', '8'],
        'poprawna': '4'
    },
    {
        'pytanie': 'Która planeta jest najbliżej Słońca?',
        'odpowiedzi': ['Wenus', 'Mars', 'Merkury'],
        'poprawna': 'Merkury'
    },
    {
        'pytanie': 'Ile boków ma trójkąt?',
        'odpowiedzi': ['3', '4', '5'],
        'poprawna': '3'
    },
    {
        'pytanie': 'Kto napisał "Pan Tadeusz"?',
        'odpowiedzi': ['Juliusz Słowacki', 'Adam Mickiewicz', 'Henryk Sienkiewicz'],
        'poprawna': 'Adam Mickiewicz'
    }
]

STATS = [0 for _ in DANE]

def shuffle_question_answers(question):
    """Przemiesza odpowiedzi w pojedynczym pytaniu"""
    answers = question['odpowiedzi'].copy()
    random.shuffle(answers)
    return {
        'pytanie': question['pytanie'],
        'odpowiedzi': answers,
        'poprawna': question['poprawna']
    }


@app.route('/', methods=['GET', 'POST'])
def index():
    """Strona główna"""
    if request.method == 'POST':
        points = 0
        answers = request.form
        current_questions = session.get('current_questions', DANE)

        for pnr, odp in answers.items():
            idx = int(pnr)
            if odp == current_questions[idx]['poprawna']:
                points += 1
                STATS[idx] += 1

        flash(f'Liczba poprawnych odpowiedzi, to: {points}/{len(DANE)}')
        return redirect(url_for('index'))

    questions = [dict(p) for p in DANE]
    random.shuffle(questions) # Losowanie pytań
    questions = [shuffle_question_answers(p) for p in questions]

    session['current_questions'] = questions

    return render_template('index.html', pytania=questions)


@app.route('/stats')
def stats():
    """Strona statystyk"""
    labels = [f"Pytanie {i+1}" for i in range(len(DANE))]
    fig = go.Figure([go.Bar(x=labels, y=STATS, marker_color='green')])
    fig.update_layout(title="Poprawne odpowiedzi na pytania", yaxis_title="Liczba poprawnych odpowiedzi")

    chartJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('stats.html', chartJSON=chartJSON)


if __name__ == '__main__':
    app.run(debug=True)
