'''
Created on Jun 18, 2015

@author: phuclt1
'''
from multiprocessing.pool import ThreadPool
import urllib.request, urllib.error, urllib.parse
import wget
import os
import sys
from bs4 import BeautifulSoup
import tqdm
import shutil

pool = ThreadPool(8)


def download_chapter(name, chaper_name, chapter_url):
    text = urllib.request.urlopen(url=chapter_url).read()
    soup = BeautifulSoup(text, 'html.parser')

    available_classes = ['reading-detail box_doc', 'content']
    for c in available_classes:
        content = soup.find('div', class_=c)
        if content:
            images = [img.attrs['src'] for img in content.find_all('img')]
            break
    print('Download {}:{}'.format(name, chaper_name))

    folder = os.path.join(name, chaper_name)
    if not os.path.exists(folder):
        os.makedirs(folder)

    for _ in tqdm.tqdm(pool.imap_unordered(lambda img: wget.download(img, out=folder, bar=None), images),
                       total=len(images)):
        pass
    print('')
    print('Compress folder {}'.format(folder))
    shutil.make_archive(os.path.join(name, chaper_name), 'zip', folder)


def download_comic(name, chapter=None):
    # Get chapter list
    text = urllib.request.urlopen('http://www.nettruyen.com/truyen-tranh/{}'.format(name)).read()
    soup = BeautifulSoup(text, 'html.parser')
    chapters = [(div.findChild('a').text, div.findChild('a').attrs['href']) for div in
                soup.find_all("div", class_="col-xs-5 chapter")]

    # Download chapter
    for c_name, c_url in chapters[::-1]:
        download_chapter(name, c_name, c_url)


if __name__ == '__main__':
    # freeze_support()

    if len(sys.argv) > 1:
        download_comic(sys.argv[1])
    else:
        print('Error parameters')
