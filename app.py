import re
from io import BytesIO

import matplotlib.pyplot as plt
from flask import Flask, render_template, redirect, request, send_file
from matplotlib import style

from twitter import MentioningCounter

app = Flask(__name__)
mentioning_counter = MentioningCounter()


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/mentioning')
def mentioning():
    words = request.args.get('words')
    if words:
        words = re.split(',\s*', words)
        return render_template('mentioning.html', words=words)
    else:
        return redirect('/')


@app.route('/graph/<word>')
def fig(word):
    mentioning = mentioning_counter.count([word]).pop(word)
    style.use('ggplot')
    dates = [str(d[0]) for d in mentioning]
    counts = [d[1] for d in mentioning]

    fig, ax = plt.subplots()
    fig.set_size_inches(10, 4)
    ax.set_ylabel('Количество упоминаний')
    ax.set_xlabel('Дата')
    ax.plot(dates, counts)

    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')


if __name__ == '__main__':
    app.run()
