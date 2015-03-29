from HTMLParser import HTMLParser
import urllib2

class CategoryParser(HTMLParser):
	features = []
	categories = []
	ignore = ["chapter", "Chapter", "Article", "Image", "image", "template", "Template", "TV", "Telltale", "icon", "page", "Icon", "help", "know"]
	done = 0
	catlinks = 0
	catlinksspan = 0
	catlinkdata = 0
	infobox = 0
	infoboxrow = 0
	infoboxcategory = 0	
	readCats = 0
	readData = 0
	categoriesToFilter = ["Allegiance","Culture","Born","Gender"]
	Allegiance = []
	Culture =[]
	Born = []
	Gender = []
	currentCategory = 0;
	
	def insert_category(self,cat,val):
		if self.cat == "Allegiance":
			self.Allegiance.append(val)
		if self.cat == "Culture":
			self.Culture.append(val)
		if self.cat == "Born":
			self.Born.append(val)
		if self.cat == "Gender":
			self.Gender.append(val)
				
	
	def handle_starttag(self, tag, attrs):
        #print tag, attrs
		if tag == "div":
			for (x,y) in attrs:
				if y == "catlinks":
					self.catlinks = 1
					
		if tag == "span":
			if self.catlinks == 1:
				self.catlinksspan = 1
		if tag == "a":
			if self.catlinksspan == 1:
				self.catlinkdata = 1
		if tag == "table":
			for (x,y) in attrs:
				if y == "infobox infobox-body":
					self.infobox = 1					
		if tag == "tr":
			if self.infobox == 1:
				self.infoboxrow = 1
				
		if tag == "th":
			if self.infoboxrow == 1:
				self.infoboxcategory = 1		
		if tag == "td":
			if self.readCats == 1:
				self.readData = 1
				
				
	def handle_endtag(self, tag):
		if tag == "div":
			if self.catlinks == 1:
				self.catlinks = 0
				
		if tag ==  "span":
			if self.catlinks == 1:
				self.catlinksspan = 0
				
		if tag == "a":
			if self.catlinksspan == 1:
				self.catlinkdata = 0
		if tag == "table":
			if self.infobox == 1:
				self.infobox = 0
				
		if tag == "tr":
			if self.infobox == 1:
				self.infoboxrow = 0
				self.infoboxcategory = 0
				self.readCats = 0
				
		if tag == "td":
			self.readData = 0
			
	def handle_data(self, data):
		if self.catlinkdata == 1:
			self.categories.append(data)
		if self.infoboxcategory == 1:
			if self.readData == 1:
				self.features.append(data)
			if self.readCats == 0:
				if data in self.categoriesToFilter:
					self.readCats = 1
	def get_categories(self):
		return self.categories
    
	def get_features(self):
		return self.features
		            
if __name__ == "__main__":
	parser = CategoryParser()
	url = "http://awoiaf.westeros.org/index.php/Arya_Stark"
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
	f = urllib2.urlopen(req)
	data = f.read()
	parser.feed(data)
	categories = parser.get_categories()
	features = parser.get_features()
	i = 1
	for category in categories:
		print str(i)+'.', category
		i+=1
	for feature in features:
		print str(i)+'.', feature
		i+=1
          
