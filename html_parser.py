'''
Created on Jun 18, 2015

@author: phuclt1
'''
from HTMLParser import HTMLParser 
from compiler.ast import Printnl

class node():
    def __init__(self, tag, attrs):
        self.tag = tag
        self.attrs = attrs
        self.children = []
        self.data = ''
    def add_child(self, child):
        self.children.append(child)

class html_parser(HTMLParser): 
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []
        self.current_tag =''
        self.current_attrs = ''
        self.start_capture = False
        self.root = node('root', 'root')
        self.new_node = None;
        self.stack = []
        self.stack.append(self.root)
        self.maps = {'root', self.root}
    
    def handle_starttag(self, tag, attrs):
        if self.new_node != None:
            self.stack.append(self.new_node)
        self.new_node = node(tag, attrs)
        if len(attrs) >= 1:
            if 'danhsach' in attrs[0][1] and 'class' in attrs[0][0]:
                #self.maps['page-select-div'] = self.new_node
                self.important = self.new_node
        
    def handle_endtag(self, tag):
        parent = self.stack.pop()
        parent.add_child(self.new_node)
        self.new_node = parent
             
        
    def handle_data(self, data):
        if self.new_node != None:
            self.new_node.data += data
        
    def printout(self):
#         print self.maps
        if self.root == None:
            print 'Emty'
        else:
            self.printNode(self.root, 0)
        
    def printNode(self, node, level):
        print '  '*level, '{<%s> <%s>: ...' %(node.tag, node.attrs)
        new_lv =level + 1
        for c in node.children:
            self.printNode(c, new_lv)
        print '  '*level, '}'
        
        
    def check(self, c, key):
        result = []
        (field, val) = key.split(':')
        if field == 'tag':
            if val == c.tag:
                return True
        elif field == 'class':
            if len(c.attrs) >= 1:
                if val in c.attrs[0][1] and 'class' in c.attrs[0][0]:
                    return True
        return False
    
    def find(self, list):
        result = []
        result.append(self.root)
        found = True
        
        for i in range(0, len(list)):
            if found:
                found = False
                new_result = []
                key = list[i]

                for root in result:
                    for c in root.children:
                        if self.check(c, key):
                                new_result.append(c)
                                found = True

                result = new_result
            else:
                return result
        return result    
