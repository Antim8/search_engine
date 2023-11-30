# hallo

import requests
from bs4 import BeautifulSoup
from whoosh.index import create_in
from whoosh.fields import *
from whoosh import index
from whoosh.qparser import QueryParser
from whoosh import scoring


# The function create_index() creates an index for the search engine.
# The index is stored in the directory "indexdir".
# The index contains the fields "url", "title" and "content".
# The field "content" contains the text of the crawled web pages.
def create_index(start_url):
    schema = Schema(url=TEXT(stored=True), title=TEXT(stored=True), content=TEXT(stored=True))
    ix = create_in("indexdir", schema)
    writer = ix.writer()

    
    crawled_urls = []
    urls_to_crawl = [start_url]

    while urls_to_crawl:
        url = urls_to_crawl.pop(0)
        response = requests.get(url)
        if 'text/html' in response.headers.get('Content-Type'):
            crawled_urls.append(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and not href.startswith('//'):
                    new_url = start_url.rstrip('/') + ('/') + href
                    if new_url not in crawled_urls and new_url not in urls_to_crawl:
                        urls_to_crawl.append(new_url)
        print("Crawled: " + url)

    for url in crawled_urls:
        response = requests.get(url)
        if 'text/html' in response.headers.get('Content-Type'):
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string
            content = soup.get_text()
            writer.add_document(url=url, title=title, content=content)
            print("Indexed: " + url)

    writer.commit()



def search(words, indexdir=""):
    if not indexdir or indexdir.isspace():
        indexdir = "indexdir"

    ix = index.open_dir(indexdir)

    # Parse the user query string
    parser = QueryParser("content", ix.schema)
    query = parser.parse(words)

    # Use BM25F scoring
    with ix.searcher(weighting=scoring.BM25F()) as searcher:
        # Try correcting the query
        corrected = searcher.correct_query(query, words)

        # Initialize variables to store suggestion and results
        suggestion = None
        results = []

        # If the corrected query is different from the original, set suggestion
        if corrected.query != query:
            suggestion = corrected.string

            # Execute the corrected query and store the results
            corrected_results = searcher.search(corrected.query)
            results = [result.fields() for result in corrected_results]

        # If the corrected query is the same as the original, just store the results for the original query
        else:
            search_results = searcher.search(query)
            results = [result.fields() for result in search_results]

        return {"suggestion": suggestion, "results": results}

        
   




if __name__ == "__main__":
   start_url = "https://vm009.rz.uos.de/crawl/"
   create_index(start_url)
    # index = crawl(start_url)
    # search_words = "platypus"
    # search_result = search(search_words, "indexdir")
    # print(search_result[0])

    #def search(words, indexdir = ""):
    #if indexdir == "" or indexdir == " ":
      #  indexdir = "indexdir"
   # ix = index.open_dir(indexdir)
    
    #with ix.searcher() as searcher:
     #   query = QueryParser("content", ix.schema).parse(words)
     #   result = searcher.search(query)



       # result_list = []
       # for r in result:
       #     result_list.append(r['url'])
       # return result_list