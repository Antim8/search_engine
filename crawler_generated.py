import requests
from bs4 import BeautifulSoup

def crawl(start_url):
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

    index = {}
    for url in crawled_urls:
        response = requests.get(url)
        if 'text/html' in response.headers.get('Content-Type'):
            soup = BeautifulSoup(response.content, 'html.parser')
            words = soup.get_text().split()
            for word in words:
                if word not in index:
                    index[word] = []
                if url not in index[word]:
                    index[word].append(url)

    return index

def search(index, words):
    result = []
    for word in words:
        if word in index:
            result.append(index[word])
    return result

if __name__ == "__main__":
    start_url = "https://vm009.rz.uos.de/crawl/"
    index = crawl(start_url)
    search_words = ["platypus"]
    search_result = search(index, search_words)
    print(search_result)