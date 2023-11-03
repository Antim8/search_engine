
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawl(start_url):
    response = requests.get(start_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for a_tag in soup.find_all('a', href=True):
        print(a_tag['href'])


if __name__ == "__main__":
    print("result of crawl")
    crawl("https://vm009.rz.uos.de/crawl/index.html")

def crawl_and_index(start_url):
    response = requests.get(start_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    index = {}
    
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
            if word not in index:
                index[word] = []
            index[word].append(url)
    
    return index

if __name__ == "__main__":
    print("result of crawl_and_index")
    index = crawl_and_index("https://vm009.rz.uos.de/crawl/index.html")
    for word, urls in index.items():
        print(f"{word}: {urls}")


def search(words, index):
    # Convert all words to lowercase (since the index is case-insensitive)
    words = [word.lower() for word in words]
    
    # Find the URLs for the first word
    urls = set(index.get(words[0], []))
    
    # For each of the other words, intersect the current set of URLs with the URLs for that word
    for word in words[1:]:
        urls &= set(index.get(word, []))
    
    return list(urls)

if __name__ == "__main__":
    print("result of search")
    words = ["mammal"]
    urls = search(words, index)
    print(urls)