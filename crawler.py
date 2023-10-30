import requests
from bs4 import BeautifulSoup


def crawl(start_url):
    index = []
    r = requests.get(start_url)
    # print(r.status_code)
    # print(r.headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    # print(soup.title.text)
    # print(soup.text)
    for l in soup.find_all("a"):
        print(l['href'])
        print(l.text)



def search(words):
    result = []
    for word in words:
        if word in index:
            result.append(index[word])
    return result

if __name__ == "__main__":
    start_url = "https://vm009.rz.uos.de/crawl/index.html"
    index = crawl(start_url)
    search_words = ["platypus", "fossil"]
    search_result = search(search_words)
    print(search_result)