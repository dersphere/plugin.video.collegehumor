import urllib2
import re
from BeautifulSoup import BeautifulSoup
from urllib import urlencode

IPAD_USERAGENT = ('Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; '
                  'en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Versi'
                  'on/4.0.4 Mobile/7B314 Safari/531.21.10')

MAIN_URL = 'http://m.collegehumor.com/'


def getCategories():
    url = MAIN_URL + 'videos/browse'
    html = __getAjaxContent(url)
    tree = BeautifulSoup(html)
    categories = list()
    for element in tree.find('ul', {'data-role': 'listview'}).findAll('a'):
        categories.append({'title': element.string,
                           'link': element['href'][1:]})
    return categories


def getVideos(category, page=1):
    post = {'render_mode': 'ajax'}
    url = MAIN_URL + '%s/page:%s' % (category, page)
    html = __getAjaxContent(url, post)
    tree = BeautifulSoup(html)
    videos = list()
    elements = tree.find('ul', {'data-role': 'listview'}).findAll('a')
    for element in elements:
        if re.search(re.compile('/video/'), element['href']):
            videos.append({'title': element.h3.string,
                           'link': element['href'][1:],
                           'image': element.img['src']})
    has_next_page = (len(elements) >= 20)
    return videos, has_next_page


def getVideoFile(link):
    url = MAIN_URL + link
    html = __getAjaxContent(url)
    tree = BeautifulSoup(html)
    return tree.find('video')['src']


def __getAjaxContent(url, data_dict=None):
    if data_dict:
        post_data = urlencode(data_dict)
    else:
        post_data = ' '
    req = urllib2.Request(url, post_data)
    req.add_header('User-Agent', IPAD_USERAGENT)
    req.add_header('Accept', ('text/html,application/xhtml+xml,'
                              'application/xml;q=0.9,*/*;q=0.8'))
    response = urllib2.urlopen(req).read()
    return response
