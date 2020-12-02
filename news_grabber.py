import requests
from bs4 import BeautifulSoup
import xmltodict
from datetime import datetime as dt


NEWS_FEEDS_CONFIG = {
    'lenta': {
        'url': 'http://lenta.ru/rss',
        'title': {'name': 'h1'},
        'image': {'class_': 'b-topic__title-image'},
        'content': {'class_': 'b-text clearfix js-topic__text'},
        'p': {'name': 'p', 'class_': None},
    },
    'interfax': {
        'url': 'http://www.interfax.ru/rss.asp',
        'encoding': 'cp1251',
        'title': {'name': 'h1'},
        'image': {'name': 'figure'},
        'content': {'name': 'article'},
        'p': {'name': 'p', 'class_': None},
    },
    'kommersant': {
        'url': 'http://www.kommersant.ru/RSS/news.xml',
        'title': {'name': 'h1'},
        'image': {'name': 'img', 'class_': 'fallback_image'},
        'content': {'class_': 'article_text_wrapper'},
        'p': {'name': 'p'}
    },
    'm24': {
        'url': 'http://www.m24.ru/rss.xml',
        'title': {'name': 'h1'},
        'image': {'class_': 'b-material-incut-m-image'},
        'content': {'class_': 'b-material-body'},
        'p': {'name': 'p', 'class_': None},
    },
}

ERROR_MSG_FEED = 'Need NEWS_FEEDS dict("name_of_feed": "url_to_feed")'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
}


def convert_date(date_string):
    date_format_in = '%a, %d %b %Y %H:%M:%S'
    date_format_out = '%d.%m.%Y %H:%M'
    date = dt.strptime(date_string.rsplit(' ', 1)[0], date_format_in)
    return date.strftime(date_format_out)


def nomalize_news(html, limit=0):
    xml_message = html.text
    newslist = xmltodict.parse(xml_message)['rss']['channel']['item']
    newslist_normalize = []
    for news in newslist:
        newslist_normalize.append({
            'title': news['title'],
            'link': news['link'],
            'desk': news['description'],
            'published': convert_date(news['pubDate']),
        })
        if len(newslist_normalize) == limit:
            break

    return newslist_normalize


def get_html(url):
    html = requests.get(url, HEADERS)
    if html.status_code == 200:
        return html
    else:
        print('Error. Cant get page. Check URL in settings and connection.')


def parse_html_to_article(html, cfg):
    if cfg.get('encoding'):
        html.encoding = cfg['encoding']
    html_text = html.text
    soup = BeautifulSoup(html_text, 'html.parser')

    title = soup.find(**cfg['title']).get_text()
    image_tag = soup.find(**cfg['image'])
    if image_tag:
        if image_tag.img:
            image = image_tag.img['src']
        else:
            # dirty hack for parsing kommersant image
            image = image_tag['src']
    else:
        image = None
    content = [p.get_text() for p in soup.find(**cfg['content']).find_all(**cfg['p'])]

    return {'title': title, 'image': image, 'content': content}


class Feed:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def news(self, limit=1):
        return nomalize_news(get_html(self.url), limit)

    def grub(self, url):
        return parse_html_to_article(get_html(url), NEWS_FEEDS_CONFIG[self.name])


class Grabber:
    def __init__(self):
        assert NEWS_FEEDS_CONFIG, ERROR_MSG_FEED
        for news in NEWS_FEEDS_CONFIG:
            setattr(self, news, Feed(news, NEWS_FEEDS_CONFIG[news]['url']))


if __name__ == '__main__':
    graber = Grabber()
    news_lenta = graber.lenta.news(limit=2)
    print(news_lenta)
    url = news_lenta[0]['link']
    data = graber.lenta.grub(url)
    print(data)
