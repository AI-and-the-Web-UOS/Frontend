from flask import Flask, render_template, request, redirect, url_for
from sent2vec.vectorizer import Vectorizer
import requests

app = Flask(__name__)


def search_embedding(search_term):
    vectorizer = Vectorizer()
    vectorizer.run([search_term])
    return vectorizer.vectors[0].tolist()


@app.route('/')
def default():
    return redirect((url_for('home')))


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('search.html')


@app.route('/results/<search_term>')
def results(search_term):
    vector = search_embedding(search_term)
    data = {
        "Vector": vector
    }

    url = "http://localhost:5001/search"
    response = requests.get(url, json=data)
    result = response.json()
    data = result["results"]
    if response.status_code == 200:
        return render_template('results.html', search_text=search_term, data=data)
    else:
        return render_template('search.html')


@app.route('/submit', methods=['POST'])
def submit():
    search_text = request.form['search_text']

    if not search_text:
        return redirect(url_for('index', error='Bitte gib einen Suchtext ein!'))

    return redirect(url_for('results', search_term=search_text))


if __name__ == '__main__':
    app.run()
