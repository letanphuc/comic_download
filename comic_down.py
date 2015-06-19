'''
Created on Jun 18, 2015

@author: phuclt1
'''
import html_parser 
import urllib2
import wget
import os
import sys

def getComicList():
    parser = html_parser.html_parser()
    f = urllib2.urlopen('http://m.blogtruyen.com/danhsach/')
    str = f.read().decode('ascii', 'ignore')
    parser.feed(str)
    node = parser.find(['tag:html', 'tag:body', 'class:wrapper', 'class:danhsach', 'class:row', 'tag:a'])
    for n in node:
        parser.printNode(n, 0)

def downloadComic(name, chapter):   
    for c in chapter:
        parser = html_parser.html_parser()
        f = urllib2.urlopen('http://m.blogtruyen.com/truyen/%s/chap-%d' %(name, c))
        str = f.read().decode('ascii', 'ignore')
        parser.feed(str)
        node = parser.find(['tag:html', 'tag:body', 'class:wrapper', 'class:noidungchap', 'tag:img'])
        
        print '  [+] Chapter %d' %c
        
        # make folder chapxxx
        folder = '%s/chap_%03d' %(name, c)
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        for i in range(0, len(node)):
            link = node[i].attrs[0][1]
            filename = '%s/%d.jpg' %(folder, i)
            if os.path.exists(filename):
                wget.download(link, out=filename, bar=None)
            percent = (i + 1) * 100 / len(node)
            sys.stdout.write('\r  [' + '-'*percent + ' '*(100- percent) + '] %d%%' %percent)
        print ''

if __name__ == '__main__':
    if len(sys.argv) > 3:
        downloadComic(sys.argv[1], range(int(sys.argv[2]), int(sys.argv[3]) + 1))
    else:
        print 'Error parametter'