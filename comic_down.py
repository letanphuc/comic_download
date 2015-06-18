'''
Created on Jun 18, 2015

@author: phuclt1
'''
import html_parser 
import urllib2

def main():
    parser = html_parser.html_parser()
    f = urllib2.urlopen('http://m.blogtruyen.com/danhsach/')
    str = f.read().decode('ascii', 'ignore')
    parser.feed(str)
    node = parser.find(['tag:html', 'tag:body', 'class:wrapper', 'class:danhsach', 'class:row', 'tag:a'])
    for n in node:
        parser.printNode(n, 0)

if __name__ == '__main__':
    main()