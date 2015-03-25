from HTMLParser import HTMLParser
import urllib2

class CategoryParser(HTMLParser):
    fieldset = 0
    ul = 0
    li = 0
    a = 0
    catname = ""
    catmem = 0
    categories = []
    ignore = ["chapter", "Chapter", "Article", "Image", "image", "template", "Template", "TV", "Telltale", "icon", "page", "Icon", "help", "know"]
    done = 0
    def handle_starttag(self, tag, attrs):
        #print tag, attrs
        if self.done == 0:
            if self.fieldset == 1:
                if tag == "ul":
                    self.ul = 1
                elif self.ul == 1:
                    if tag == "li":
                        self.li = 1
                    elif self.li == 1:
                        if tag == "a":
                            self.a = 1
                        
    def handle_endtag(self, tag):
        if self.done == 0:
            if tag == "fieldset":
                self.fieldset = 1
            if self.ul == 1:
                if tag == "a":
                    self.a = 0
                if tag == "ul":
                    self.categories = sorted(self.categories, key=lambda x: x[0], reverse=True)
                    self.done = 1
                    
    def handle_data(self, data):
        if self.done == 0:
            if self.ul == 1:
                if self.a == 1:
                    self.catname = data
                    #print "$$$$$", self.catname
                elif self.li == 1:
                    self.catmem = data
                    #print "*****", self.catmem
                    #print self.catmem.strip("() members")
                    self.catmem = int(self.catmem.strip("() members").replace(',', ''))
                    #print self.catmem
                    if self.catmem > 9:
                        flag = 0
                        for ig in self.ignore:
                            if ig in self.catname:
                                flag = 1
                                break
                        if flag == 0:
                            self.categories.append((self.catmem, self.catname))
                            #print (self.catmem, self.catname)
                    self.li = 0
                
    def get_categories(self):
        return self.categories
                
if __name__ == "__main__":
    parser = CategoryParser()
    url = "http://awoiaf.westeros.org/index.php?title=Special:Categories&limit=10000"
    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
    f = urllib2.urlopen(req)
    data = f.read()
    parser.feed(data)
    categories = parser.get_categories()
    
    i = 1
    for category in categories:
        print str(i)+'.', category
        i+=1
            
