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
	readChapterName = 0
	readChapterNumber = 0
	readAllegiance = 0
	readCulture = 0
	readBorn = 0
	readDied = 0
	readGender = 0
	catIndex = 0
	categoriesToFilter = ["Allegiance","Culture","Born","Gender","Died"]
	Allegiance = []
	Culture =[]
	Born = []
	Gender = []
	Died = []
	chapterReferences = []
	currentCategory = 0
	chapters = 0
	chapter_name = 0
	chap = ""
	chapter_number = 0
	
				
	
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
			if self.chapter_name == 1:
				self.readChapterName = 1
			if self.chapters == 1:
				if self.chapter_name == 0:
					self.readChapterNumber = 1		
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
		
		if tag == "span":
				for (x,y) in attrs:
					if y == "reference-text":
						self.chapters = 1
		if tag == "i":
			if self.chapters == 1:
				self.chapter_name = 1					
				
	def handle_endtag(self, tag):
		if tag == "div":
			if self.catlinks == 1:
				self.catlinks = 0
				
		if tag ==  "span":
			if self.catlinks == 1:
				self.catlinksspan = 0
			if self.chapters == 1:	
				self.chapters = 0
				
		if tag == "a":
			if self.catlinksspan == 1:
				self.catlinkdata = 0
			self.readChapterName = 0
			self.readChapterNumber = 0
					
		if tag == "table":
			if self.infobox == 1:
				self.infobox = 0
				
		if tag == "tr":
			if self.infobox == 1:
				self.infoboxrow = 0
				self.infoboxcategory = 0
				self.readCats = 0
				self.readAllegiance = 0
				self.readCulture = 0
				self.readBorn = 0
				self.readGender = 0
				
		if tag == "td":
			self.readData = 0
		
		if tag == "i":
			if self.chapter_name == 1:
				self.chapter_name = 0
				
	def handle_data(self, data):
		if self.readCats == 1:
			if self.readAllegiance == 1:
				self.Allegiance.append(data.strip(' \t\n\r'))
			if self.readCulture == 1:
				self.Culture.append(data.strip(' \t\n\r'))
			if self.readBorn == 1:
				self.Born.append(data.strip(' \t\n\r'))
			if self.readGender == 1:
				self.Gender.append(data.strip(' \t\n\r'))
			if self.readDied == 1:
				self.Died.append(data.strip(' \t\n\r'))	
						
		if self.infoboxcategory == 1:
			if self.readData == 1:
				self.features.append(data)
			if self.readCats == 0:
				if data in self.categoriesToFilter:
					self.readCats = 1
					if data in "Allegiance":
						self.readAllegiance = 1
						print "Allegiance detected"
					if data in "Culture":	
						self.readCulture = 1
					if data in "Born":
						self.readBorn = 1
					if data in "Gender":
						self.readGender = 1
					if data in "Died":
						self.readDied = 1		
								
		if self.readChapterName == 1:
			self.chap = data
		if self.readChapterNumber == 1:
			self.chapterReferences.append((self.chap.strip(' \t\n\r'),data.strip(' \t\n\r')))	
					
	def get_categories(self):
		return self.categories
    
	def get_features(self):
		return self.features
	def get_chapterReferences(self):
		return self.chapterReferences
	def get_allegiance(self):
		return self.Allegiance
	def get_culture(self):
		return self.Culture
	def get_born(self):
		return self.Born	
	def get_gender(self):
		return self.Gender
	def get_died(self):
		return self.Died
			
	def extract_data(self,character_name):
		parser = CategoryParser()
		url = "http://awoiaf.westeros.org/index.php/"+character_name
		req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
		f = urllib2.urlopen(req)
		data = f.read()
		parser.feed(data)
		categories = parser.get_categories()
		features = parser.get_features()
		chapterrefs = parser.get_chapterReferences()
		allegiance = parser.get_allegiance()
		culture = parser.get_culture()
		gender = parser.get_gender()
		born = parser.get_born()
		died = parser.get_died()
		
		ChapterReferences = []
		for (chapname,no) in chapterrefs:
			if "Chapter" in no:
				ChapterReferences.append((chapname,no))
		
		BirthDate = 'NULL'
		for bdate in born:
			for bday in bdate.split():
				if bday.isdigit() and len(bday) >=3:
					BirthDate = bday
		DeathDate = 'NULL'
		for bdate in died:
			for bday in bdate.split():
				if bday.isdigit() and len(bday) >=3:
					DeathDate = bday
					
		
			
		
		return (ChapterReferences,allegiance,culture,BirthDate,DeathDate)
		
if __name__ == "__main__":
	parser = CategoryParser()
	file = '../Data/character_names.txt'	
	f = open(file, 'r')
	j = 1
	if(f):
		 for line in f:
			print str(j) +'.'+ line
			(ChapterReferences,allegiance,culture,BirthDate,DeathDate) = parser.extract_data(line)
			 ## Chapter references	
				
			print "Chapter references :"
			for (a,b) in ChapterReferences:
				print a+','+b
				  	
			print "Allegiance :"
			# Allegiance	
			for a in allegiance:
				print  a
				
			print "Culture :"
			# Culture	
			for a in culture:
				print a
				
			# Born	
			print "Born : "+ BirthDate
		
			# Died	
			print "Died : "+ DeathDate	
			j+=1
	f.close()	
	
