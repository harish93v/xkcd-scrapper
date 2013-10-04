from bs4 import BeautifulSoup
from urllib2 import urlopen
from urllib import urlretrieve
from joblib import Parallel, delayed
import os
import sys
import io
import re
import lxml
from lxml.html.clean import Cleaner
import codecs
import string
import time

base_url = "http://www.xkcd.com/"


def down_links(directory, start=1, end=1):
    # Leave 404 because it is a 404 page
    start = int(start)
    end = int(end) + 1  # To include end in result
    links = [[directory + (base_url + str(i)).split("/")[-1] + '/', base_url + str(i)]
             for i in range(start, end) if i != 404]
    return links


def down_content(url, directory='/tmp/xkcd'):
    if os.path.exists(directory):
        return
    html = urlopen(url).read()
    soup = BeautifulSoup(html)
    if soup.find("div", {"id": "ctitle"}).string:
        title = (soup.find("div", {"id": "ctitle"})).string.strip()
    else:
        title = (soup.find("div", {"id": "ctitle"})).span.string.strip()
    title = ''.join(filter(lambda x: x in string.printable, title))
    title = re.sub('[.!/;]', '', title)
    img_section = soup.find("div", {"id": "comic"})
    if not img_section.img['src']:
        img_url = img_section.noscript.img['src']
        img_text = unicode(img_section.noscript.img['title'])
    else:
        img_url = img_section.img['src']
        img_text = unicode(img_section.img['title'])
    img_name = title + '.' + img_url.split('.')[-1]
    os.makedirs(directory)
    imgpath = os.path.join(directory, img_name)
    textfile = os.path.join(directory, title + '.txt')
    f = codecs.open(textfile, 'w', encoding='utf-8')
    f.write(img_text)
    print "Fetching image: " + unicode(title)
    urlretrieve(img_url, imgpath)
    print "Done with downloading" + url + "Check at" + directory

if __name__ == '__main__':
    start_time = time.time()
    start = 1
    end = 1244
    no_jobs = 1
    if len(sys.argv) >= 2:
        start = sys.argv[1]
    if len(sys.argv) >= 3:
        end = sys.argv[2]
    if len(sys.argv) >= 4:
        no_jobs = int(sys.argv[3])
    directory = '/tmp/xkcd'
    print "Let the game begin!"
    links = down_links(directory, start, end)
    Parallel(n_jobs=no_jobs)(
        delayed(down_content)(link[1], link[0]) for link in links)
    print time.time() - start_time, "seconds"
