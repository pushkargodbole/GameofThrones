import csv

s = {}

with open('../Data/status.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for line in reader:
		t = line['occupations']
		s[str(t)] = 1
		#print t
#print s
with open('t.csv') as csvfile:
	op = ""
	reader = csv.DictReader(csvfile)
	k = 0
	for row in reader:
		k = k + 1
		occupations = []
		for i in range(1,16):
			#print row[str(i)]
			if row[str(i)] in s:
				occupations.append(row[str(i)])
			else:
				pass
		csvline = ""
		for j in range(0,len(occupations)):	
			csvline+= occupations[j].strip("\n")+"#"
		#csvline += "\n"
		print csvline
		#for x in c:
		#	print x + ","
		#print "\n"
	

