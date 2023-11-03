from flask import Flask, render_template, request, redirect, url_for
from sent2vec.vectorizer import Vectorizer

vectorizer = Vectorizer()
app = Flask(__name__)


def search_embedding(search_term):
    vectorizer.run([search_term])
    return vectorizer.vectors


@app.route('/')
def default():
    return redirect((url_for('home')))


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        search_term = request.form.get('search_term')
        vector = search_embedding(search_term)
        return redirect(url_for('results', search_term=search_term))
    return render_template('search.html')


@app.route('/results/<search_term>')
def results(search_term):
    return render_template('results.html', search_term=search_term)


if __name__ == '__main__':
    app.run()
