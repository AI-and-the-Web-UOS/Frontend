from flask import Flask, render_template, request, redirect, url_for
from sent2vec.vectorizer import Vectorizer
import requests
from embedding import EmbeddingManager

app = Flask(__name__)

URL = "http://localhost:5001/search"
embeddingManager = EmbeddingManager()


def search_embedding(search_term):
    """
    Embeds the given search term using Sent2Vec vectorization.

    :param search_term: The search term to be embedded.
    :return: The vector representation of the search term.
    """

    vectorizer = Vectorizer()  # Create a Sent2Vec Vectorizer
    vectorizer.run([search_term])  # Run the vectorization process on the given search term
    return vectorizer.vectors[0].tolist()  # Retrieve the vector representation of the search term


@app.route('/')
def default():
    """
    Redirects to the home page.

    :return: Redirects to the home page.
    """

    return redirect(url_for('home'))


@app.route('/home', methods=['GET', 'POST'])
def home():
    """
    Renders the search page template.

    :return: Renders the 'search.html' template.
    """

    return render_template('search.html')


@app.route('/results/<search_term>')
def results(search_term):
    """
    Retrieves search results from an external API based on the vector representation
    of the given search term.

    :param search_term: The search term for which results are requested.
    :return: Renders the 'results.html' template with search results.
    """

    embeddingManager.add_query(search_term)
    while search_term not in embeddingManager.result_dict.keys():
        pass

    # vector = search_embedding(search_term)  # Get the vector representation of the search term

    # Prepare data to be sent to the search API
    data = {
        # "Vector": vector
        "Vector": embeddingManager.result_dict[search_term]
    }

    response = requests.get(URL, json=data)  # Send a GET request to the search API with the vector data
    result = response.json()  # Parse the JSON response from the search API
    data = result["results"]  # Extract the search results from the API response

    # Check if the API request was successful (status code 200)
    if response.status_code == 200:
        # Render the results page template with the search text and data
        return render_template('results.html', search_text=search_term, data=data)
    else:
        # If there was an error with the API request, redirect back to the search page
        return render_template('search.html')


@app.route('/submit', methods=['POST'])
def submit():
    """
    Handles form submission, redirects to the results page if a search text is provided,
    and redirects to the search page with an error message if the search text is empty.

    :return: Redirects to the appropriate page.
    """

    search_text = request.form['search_text']  # Get the search text from the submitted form

    # Check if the search text is empty and redirect to the appropriate template
    if not search_text:
        return redirect(url_for('index', error='Bitte gib einen Suchtext ein!'))

    return redirect(url_for('results', search_term=search_text))


if __name__ == '__main__':
    app.run()
