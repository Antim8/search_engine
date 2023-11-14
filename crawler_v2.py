import requests
from bs4 import BeautifulSoup
from whoosh.index import create_in
from whoosh.fields import *
from whoosh import index
from whoosh.qparser import QueryParser

# The function create_index() creates an index for the search engine.
# The index is stored in the directory "indexdir".
# The index contains the fields "url", "title" and "content".
# The field "content" contains the text of the crawled web pages.
def create_index(start_url):
    schema = Schema(url=TEXT(stored=True), title=TEXT(stored=True), content=TEXT)
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

    for url in crawled_urls:
        response = requests.get(url)
        if 'text/html' in response.headers.get('Content-Type'):
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string
            content = soup.get_text()
            writer.add_document(url=url, title=title, content=content)

    writer.commit()

def search(words, indexdir = ""):
    if indexdir == "" or indexdir == " ":
        indexdir = "indexdir"
    ix = index.open_dir(indexdir)
    
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(words)
        result = searcher.search(query)
        return result
    # result = []
    # for word in words:
    #     if word in index:
    #         result.append(index[word])
    # return result

if __name__ == "__main__":
    start_url = "https://vm009.rz.uos.de/crawl/"
    create_index(start_url)
    # index = crawl(start_url)
    search_words = "platypus"
    search_result = search(search_words, "indexdir")
    print(search_result)