from flask import Flask, request, render_template
from whoosh.qparser import QueryParser
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from whoosh import index, fields, writing
from whoosh.filedb.filestore import RamStorage

app = Flask(__name__)

schema = fields.Schema(word=fields.TEXT(stored=True), url=fields.ID(stored=True))
storage = RamStorage()
idx = storage.create_index(schema)

def crawl_and_index_whoosh(start_url):
    writer = idx.writer()
    response = requests.get(start_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for a_tag in soup.find_all('a', href=True):
        url = a_tag['href']
        if not url.startswith('http'):
            url = urljoin(start_url, url)
        try:
            page_response = requests.get(url)
        except requests.exceptions.RequestException:
            continue
        page_soup = BeautifulSoup(page_response.text, 'html.parser')
        words = page_soup.get_text().split()
        for word in words:
            word = word.lower()
            writer.add_document(word=word, url=url)
    writer.commit()

crawl_and_index_whoosh("https://vm009.rz.uos.de/crawl/index.html")

@app.route('/')
def home():
    return render_template('search.html')

@app.route('/search')
def search():
    query_string = request.args.get('q', '')
    results = []
    if query_string:
        with idx.searcher() as searcher:
            query = QueryParser("word", idx.schema).parse(query_string)
            results = searcher.search(query)
    return render_template('results.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)
