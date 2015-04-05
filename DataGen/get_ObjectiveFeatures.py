from HTMLParser import HTMLParser
import urllib2

class CategoryParser(HTMLParser):
    features = []
    categories = []
    ignore = ["chapter", "Chapter", "Article", "Image", "image", "template", "Template", "TV", "Telltale", "icon", "page", "Icon", "help", "know"]
    books = {"A Game of Thrones":1, "A Clash of Kings":2, "A Storm of Swords":3, "A Feast for Crows":4, "A Dance with Dragons":5}
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
    ExtractedData = {}
                
    def initialize_data(self):
        self.features = []
        self.categories = []
        self.ignore = ["chapter", "Chapter", "Article", "Image", "image", "template", "Template", "TV", "Telltale", "icon", "page", "Icon", "help", "know"]
        self.done = 0
        self.catlinks = 0
        self.catlinksspan = 0
        self.catlinkdata = 0
        self.infobox = 0
        self.infoboxrow = 0
        self.infoboxcategory = 0    
        self.readCats = 0
        self.readData = 0
        self.readChapterName = 0
        self.readChapterNumber = 0
        self.readAllegiance = 0
        self.readCulture = 0
        self.readBorn = 0
        self.readDied = 0
        self.readGender = 0
        self.catIndex = 0
        self.categoriesToFilter = ["Allegiance","Culture","Born","Gender","Died"]
        self.Allegiance = []
        self.Culture =[]
        self.Born = []
        self.Gender = []
        self.Died = []
        self.chapterReferences = []
        self.currentCategory = 0
        self.chapters = 0
        self.chapter_name = 0
        self.chap = ""
        self.chapter_number = 0
        
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
                self.Allegiance.append(data.strip(' \t\r').replace("\n",""))
            if self.readCulture == 1:
                self.Culture.append(data.strip(' \t\r').replace("\n",""))
            if self.readBorn == 1:
                self.Born.append(data.strip(' \t\n\r').replace("\n",""))
            if self.readGender == 1:
                self.Gender.append(data.strip(' \t\r').replace("\n",""))
            if self.readDied == 1:
                self.Died.append(data.strip(' \t\r').replace("\n",""))    
                        
        if self.infoboxcategory == 1:
            if self.readData == 1:
                self.features.append(data)
            if self.readCats == 0:
                if data in self.categoriesToFilter:
                    self.readCats = 1
                    if data in "Allegiance":
                        self.readAllegiance = 1
                        
                    if data in "Culture":    
                        self.readCulture = 1
                    if data in "Born":
                        self.readBorn = 1
                    if data in "Gender":
                        self.readGender = 1
                    if data in "Died":
                        self.readDied = 1        
                                
        if self.readChapterName == 1:
            self.chap = data.replace("\n","")
        if self.readChapterNumber == 1:
            self.chapterReferences.append((self.chap.strip(' \t\n\r').replace("\n",""),data.strip(' \t\n\r').replace("\n","")))    
                    
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
    
    def extract_data_from_csv(self):
        import csv
        reader = ''
        dataFromCSV = []
        with open('../Data/character_attributes.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                dataFromCSV.append(row)
    
        # Clean data    
        for row in dataFromCSV:
            self.ExtractedData[row["Character"].replace(row["Title"],"").replace(row["Old Surname"],"").replace("()","").replace(row["Alias"],"").replace(",","").replace("\n","").replace(" ","").replace("_","").lower()] = (row["Gender"],row["Status"],row["POV"])    
    
    def extract_data(self,character_name):
       
        
        parser = CategoryParser()
        parser.initialize_data()
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
        
        born = parser.get_born()
        died = parser.get_died()
        
        ChapterReferences = []
        for (chapname,no) in chapterrefs:
            if "Chapter" in no:
                try:
                    ChapterReferences.append((self.books[chapname],int(no.strip('Chapter '))))
                except:
                    pass        
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
                    
        Gender = ''
        Status = ''
        POV = ''
        
        dictkey = character_name.replace("\n","").replace(" ","").replace("_","").replace(",","").lower() 
        
        
        ##print "checking "+character_name+" dkey is : "+dictkey
            
        if dictkey in self.ExtractedData.keys():    
            (Gender,Status,POV) = self.ExtractedData[dictkey]

        return (ChapterReferences,allegiance,culture,BirthDate,DeathDate,Gender,Status,POV)
        
if __name__ == "__main__":
    parser = CategoryParser()
    parser.extract_data_from_csv()
    file = '../Data/character_names.txt'    
    chapters = [73, 70, 82, 46, 73]
    data = {'Type': 'References', 'Characters':[]}
    f = open(file, 'r')
    j = 0
    if(f):
         for line in f:
            print str(j) +'.'+ line
            (ChapterReferences,allegiance,culture,BirthDate,DeathDate,Gender,Status,POV) = parser.extract_data(line)
             ## Chapter references    
                
            data['Characters'].append({'Name':line.strip(' \n\t\r').replace('_', ' '), 'ref':[]})
            for (a,b) in ChapterReferences:
                data['Characters'][j]['ref'].append((a-1)*chapters[a-1]+b)
            print data['Characters'][j]
                      
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
            
            #Gender
            print "Gender : "+Gender
            
            #Status
            print "Status : "+Status
            
            #POV
            print "POV : "+POV
    
                
            j+=1
    f.close()
    
    reffilename = "References.json"
    reffile = open(reffilename, 'w') 
    json.dump(data, reffile, indent=4, separators=(',', ':'), ensure_ascii=False, skipkeys=True)
    reffile.close()     
    
