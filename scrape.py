import requests
import urllib.request
import time
from bs4 import BeautifulSoup

url = 'https://www.gutenberg.org/browse/scores/top'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
items = soup.ol.findAll('li')

links = []

for i in items:
    a = i.find('a')
    links.append('https://www.gutenberg.org' + a['href'])
    time.sleep(0.1)

d_links = {}

for l in links:
    d_response = requests.get(l)
    d_soup = BeautifulSoup(d_response.text, 'html.parser')
    if d_soup.find('a', type="text/plain; charset=utf-8"):
        a = d_soup.find('a', type="text/plain; charset=utf-8")
        title = d_soup.h1.get_text().replace(':', '-')
        d_links[title] = 'https:' + a['href']
    elif d_soup.find('a', type="text/plain"):
        a = d_soup.find('a', type="text/plain")
        title = d_soup.h1.get_text().replace(':', '-')
        d_links[title] = 'https:' + a['href']
    else:
        pass

for title,url in d_links.items():
    urllib.request.urlretrieve(url, '/Users/Chris/Books/' + title + '.txt')
    print('Book (' + title + ') Saved.')
