'''
Created on Jun 18, 2015

@author: phuclt1
'''
import html_parser
import urllib.request, urllib.error, urllib.parse
import wget
import os
import sys


def printBar(percent):
    total = 50
    first = total * percent / 100
    second = total - first
    sys.stdout.write('\r  [' + '-' * first + ' ' * second + '] %d%%' % percent)
    sys.stdout.flush()


def getComicList():
    parser = html_parser.html_parser()
    f = urllib.request.urlopen('http://m.blogtruyen.com/danhsach/')
    str = f.read().decode('ascii', 'ignore')
    parser.feed(str)
    node = parser.find(['tag:html', 'tag:body', 'class:wrapper', 'class:danhsach', 'class:row', 'tag:a'])
    for n in node:
        parser.printNode(n, 0)


def downloadComic(name, chapter):
    for c in chapter:
        parser = html_parser.html_parser()
        str = urllib.request.urlopen('http://m.blogtruyen.com/truyen/%s/chap-%d' % (name, c)).read()
        parser.feed(str)
        parser.fix()

        node = parser.find(['tag:html', 'tag:body', 'class:wrapper', 'id:ads', 'class:noidungchap', 'tag:img'])

        print('  [+] Chapter %d' % c)

        # make folder chapxxx
        folder = '%s/%03d' % (name, c)
        if not os.path.exists(folder):
            os.makedirs(folder)

        for i in range(0, len(node)):
            link = node[i].attrs[0][1]
            filename = '%s/' % (folder)
            wget.download(link, out=filename, bar=None)
            percent = (i + 1) * 100 / len(node)
            printBar(percent)
        print('')


if __name__ == '__main__':
    if len(sys.argv) > 3:
        downloadComic(sys.argv[1], list(range(int(sys.argv[2]), int(sys.argv[3]) + 1)))
    else:
        print('Error parametter')
