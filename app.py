from flask import Flask, render_template, request, redirect, url_for, jsonify
from sent2vec.vectorizer import Vectorizer
import requests
from embedding import EmbeddingManager

app = Flask(__name__)

URL_SEARCH = "http://localhost:5001/search"
URL_ADDVIEW = "http://localhost:5001/addView"
embeddingManager = EmbeddingManager()


def search_embedding(search_term):
    """
    Embeds the given search term using Sent2Vec vectorization.

    :param search_term: The search term to be embedded.
    :return: The vector representation of the search term.
    """

    vectorizer = Vectorizer('distilbert-base-multilingual-cased')  # Create a Sent2Vec Vectorizer
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

    error = None

    if 'error' in request.args:  # Check if an error should be displayed
        error = request.args['error']

    return render_template('search.html', error=error)


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

    try:
        response = requests.get(URL_SEARCH, json=data)  # Send a GET request to the search API with the vector data
        result = response.json()  # Parse the JSON response from the search API
        data = result["results"]  # Extract the search results from the API response
        # Render the results page template with the search text and data
        return render_template('results_new.html', search_text=search_term, data=data)
    except:
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
        return redirect(url_for('home', error='Please enter a search term!'))

    return redirect(url_for('results', search_term=search_text))

@app.route('/addView', methods=['POST'])
def add_view():
    """
    This function acts like a middleware for transmitting request from html template to search server

    :return: request status
    """

    # Get the JSON data from the request
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    # Send request to search server that given url has been clicked by user
    try:
        requests.post(URL_ADDVIEW, json=data)
    except Exception as e:
        print(f"An error occurred: {e}")

    return "", 200


if __name__ == '__main__':
    app.run()
