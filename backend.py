# backend.py
import crawler
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    query = request.args['q']
    return render_template('search.html', q = query, result = crawler.search(query.split()))