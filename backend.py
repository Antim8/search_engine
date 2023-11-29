import crawler_v2
from flask import Flask, request, render_template

app = Flask(__name__)

def perform_search(query):
    result = crawler_v2.search(query)
    suggestion, results = result.get("suggestion"), result.get("results", [])
    print(f"Query: {query}, Suggestion: {suggestion}, Results: {results}")
    return suggestion, results

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    query = request.args['q']
    suggestion, results = perform_search(query)
    return render_template('search.html', q=query, suggestion=suggestion, results=results)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=2000, debug=True)
