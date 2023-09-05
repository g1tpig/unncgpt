import sys
import requests
from bs4 import BeautifulSoup
import json
import time
import random
import os

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
]

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

def getHtml(url):
    time.sleep(5)
    retry_count = 5
    proxy = get_proxy().get("proxy")
    user_agent = random.choice(user_agents)
    headers = {'User-Agent': user_agent}
    while retry_count > 0:
        try:
            html = requests.get(url, proxies={"http": "http://{}".format(proxy)}, headers=headers)
            return html
        except Exception:
            retry_count -= 1
    delete_proxy(proxy)
    return None

def get_texts_from_link(link):
    # Send a GET request to the link
    response = getHtml(link)
    response.raise_for_status()

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the "t_f" class texts
    texts = []
    for tag in soup.find_all(class_ = "t_f"):
        texts.append(tag.text)
        print(tag.text)
    return texts

def crawl_main_page(url):
    # Send a GET request to the URL
    response = getHtml(url)
    response.raise_for_status()

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the "s xst" class links
    base_url = "https://www.1point3acres.com/bbs/"
    links = [(base_url + tag['href']) for tag in soup.find_all(class_='s xst', href=True)]

    # Iterate through the links and get the texts from "t_f" class
    data = []
    for link in links:
        texts = get_texts_from_link(link)
        data.append({
            'link': link,
            'question': texts[0],
            'comments': [{'comment': comment} for comment in texts[1:]]
        })

    return data

# URL to crawl
url = 'https://www.1point3acres.com/bbs/forum-27-1.html'

# Crawl the main page and get the data
data = crawl_main_page(url)

# Write to a JSON file
max_size = 5 * 1024 * 1024 * 1024
with open('1point3_liuxueshenqing.json', 'w', encoding='utf-8') as file:
    for item in data:
        if os.path.getsize('1point3_liuxueshenqing.json') >= max_size:
            print('文件过大,停止程序')
            sys.exit(0)
        json.dump(item, file, ensure_ascii=False, indent=4)

print("Crawling completed. Data saved to output.json")
