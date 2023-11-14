import threading
from sent2vec.vectorizer import Vectorizer

class EmbeddingManager:
    def __init__(self):
        self.query_dict = {}  # Dictionary to store queries that need to be converted
        self.result_dict = {}  # Dictionary to store the resulting vectors
        self.vectorizer = Vectorizer()
        self.lock = threading.Lock()  # Lock to ensure thread safety
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def add_query(self, query):
        with self.lock:
            self.query_dict[query] = None  # Add query to the dictionary with a placeholder for the result

    def convert_query(self, query):
        with self.lock:
            self.vectorizer.run([query])
            self.result_dict[query] = self.vectorizer.vectors[0].tolist()  # Store the result in the dictionary
            del self.query_dict[query]  # Remove the query from the conversion dictionary

    def run(self):
        while True:
            with self.lock:
                queries_to_convert = list(self.query_dict.keys())  # Make a copy of keys to avoid dict size changing during iteration

            for query in queries_to_convert:
                self.convert_query(query)

    def start_thread(self):
        thread = threading.Thread(target=self.run)
        thread.daemon = True  # Daemonize the thread so it will be terminated when the main program exits
        thread.start()