import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
from gne import GeneralNewsExtractor
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import redis

start_url = 'https://www.nottingham.edu.cn/cn/'
MAX_DEPTH = 10
MAX_THREADS = 20
filtered_extensions = ['.mp4', '.avi', '.pdf', '.zip', '.exe']

def sameDomain(url_to_check, base_url):
    base_parsed = urlparse(base_url)
    url_parsed = urlparse(url_to_check)
    return url_parsed.scheme == base_parsed.scheme and url_parsed.hostname == base_parsed.hostname

def clean_url(url):
    # 去除锚点
    parts = urlparse(url)
    # 使用urlunparse来重新构造URL，但不包括fragment部分
    return urlunparse((parts.scheme, parts.netloc, parts.path, parts.params, parts.query, ""))

def process_url(url, depth):
    print(f'Crawling {url} at depth {depth}')
    # 获得渲染过后的html
    try:
        driver.get(url)
    except WebDriverException as e:
        print(f"An error occurred while trying to access {url}: {e}")
        return
    driver.implicitly_wait(10)
    html = driver.page_source
    # 解析html的标题、发布时间、内容、图片
    extractor = GeneralNewsExtractor()
    try:
        parse_result = extractor.extract(html, noise_node_list=['//div[@class="comment-list"]'])
        if parse_result['title'] == '404' or parse_result['title'] == '隐私设置错误':
            parse_result = None
        else:
            modified_image = []
            for image in parse_result['images']:
                modified_image.append(urljoin(url, image))
            parse_result['images'] = modified_image
    except Exception as e:
        print(f"Parsing failed: {e}")
        parse_result = None
    result.append(parse_result)
    soup = BeautifulSoup(html, 'html.parser')
    new_urls = []
    for tag in soup.findAll('a', href=True):
        tag_url = urljoin(url, tag['href'])
        tag_url = clean_url(tag_url)
        # 过滤爬过的网页
        if (redis_client.sismember('crawled_urls', tag_url.lower())) or not sameDomain(tag_url, start_url):
            continue
        # 过滤PDF网页
        if tag_url.endswith('.pdf'):
            continue
        # 过滤无效网页
        parsed_url = urlparse(tag_url)
        if parsed_url.path[:11] == "/en/persons":
            continue
        new_urls.append((tag_url, depth + 1))
    return new_urls

def crawl(url, depth):
    urls_to_crawl = Queue()
    urls_to_crawl.put((url, depth))
    redis_client.sadd('crawled_urls', url.lower())
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        while not urls_to_crawl.empty():
            url, depth = urls_to_crawl.get(block=True, timeout=None)
            if depth > MAX_DEPTH:
                continue
            new_urls = executor.submit(process_url, url, depth).result()
            for new_url, new_depth in new_urls:
                if redis_client.sismember('crawled_urls', new_url.lower()):
                    continue
                redis_client.sadd('crawled_urls', new_url.lower())
                urls_to_crawl.put((new_url, new_depth), block=True, timeout=None)

if __name__ == '__main__':
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
    crawled_urls = set()
    result = []
    options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    try:
        redis_client.delete('crawled_urls')
        crawl(start_url, 0)
    finally:
        driver.quit()
        redis_client.delete('crawled_urls')
        with open('content/nottingham_cn_1.json', 'a') as json_file:
            json.dump(result, json_file, ensure_ascii=False, indent=4)
