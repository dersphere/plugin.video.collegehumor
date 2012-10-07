import urllib2
import re
from BeautifulSoup import BeautifulSoup
from urllib import urlencode

IPAD_USERAGENT = (
    'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; '
    'en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Versi'
    'on/4.0.4 Mobile/7B314 Safari/531.21.10'
)

MAIN_URL = 'http://m.collegehumor.com/'


def getCategories():
    url = MAIN_URL + 'videos/browse'
    tree = __getTree(url)
    categories = []
    for a in tree.find('ul', {'data-role': 'listview'}).findAll('a'):
        categories.append({
            'title': a.string,
            'link': a['href'][1:]
        })
    return categories


def getVideos(category, page=1):
    post = {'render_mode': 'ajax'}
    url = MAIN_URL + '%s/page:%s' % (category, page)
    tree = __getTree(url, post)
    videos = []
    for a in tree.find('ul', {'data-role': 'listview'}).findAll('a'):
        videos.append({
            'title': a.h3.string,
            'link': a['href'][1:],
            'image': a.img['src']
        })
    has_next_page = len(videos) == 24
    return videos, has_next_page


def getVideoFile(link):
    re_youtube = re.compile('http://www.youtube.com/embed/(\w+)')
    url = MAIN_URL + link
    tree = __getTree(url)
    if tree.find('video'):
        playback_url = tree.find('video').get('src')
    elif tree.find('iframe', {'src': re_youtube}):
        youtube_iframe = tree.find('iframe', {'src': re_youtube})
        yotube_id = re.search(re_youtube, youtube_iframe['src']).group(1)
        playback_url = ('plugin://plugin.video.youtube/'
                        '?action=play_video&videoid=%s' % yotube_id)
    else:
        pass
        # Houston, we have a problem
    return playback_url


def __getTree(url, data_dict=None):
    print url
    if data_dict:
        post_data = urlencode(data_dict)
    else:
        post_data = ' '
    req = urllib2.Request(url, post_data)
    req.add_header('User-Agent', IPAD_USERAGENT)
    req.add_header('Accept', ('text/html,application/xhtml+xml,'
                              'application/xml;q=0.9,*/*;q=0.8'))
    response = urllib2.urlopen(req).read()
    tree = BeautifulSoup(response, convertEntities=BeautifulSoup.HTML_ENTITIES)
    return tree
