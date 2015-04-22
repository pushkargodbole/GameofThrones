import json
import csv
from pprint import pprint
from get_personalities import get_personalities
from nltk import PorterStemmer

with open( subjectiveFeatures.json ) as data_file:    
    data = json.load(data_file)


physical_features = [ hair , eyes , face , beard , skin , flesh ,  accent ,  nose , legs ,  shoulders , stomach , jaw , ears , nipples , laugh , smile , lips , cheekbones , height , chin , mustache , scales , build , voice , eyebrows , appetite , chest , grasp , temper , figure , hairs , tongue , mouth , hands , bosom , breasts , belly , whiskers , cheeks , size , body ]
personality_stems = []


personalities = get_personalities([ ../Data/traits1.txt ,  ../Data/traits2.txt ])
used_personalities = []

objective_characteristics = [ Allegiance , Culture , Birthyear , Deathyear , Age, Gender , DeadAlive ]


	#for row in reader:
	#	print(row[ Character name ], row[ Deathyear ])
	#print reader[ Character name ]


with open( characteristics.csv ,  ab ) as csvfile:
	spamwriter = csv.writer(csvfile, delimiter= , , quotechar= | , quoting=csv.QUOTE_MINIMAL)
	spamwriter.writerow([ Name ]+personalities+objective_characteristics)

   	for character in data["Characters"]:
		#print character["Name"],", "
		char_personality = [None]*len(personalities)
		char_objective = [None]*len(objective_characteristics)
		for personality in personalities:
			if personality in character["Characteristics"]:
				used_personalities.append(personality)
				#print personality,character["Characteristics"][personality],str(PorterStemmer().stem_word(personality).lower())
				if character["Characteristics"][personality] != None:
					char_personality[personalities.index(personality)] = int(character["Characteristics"][personality])

		with open( character_features.csv ) as csvfile2:
			reader = csv.DictReader(csvfile2)
			for row in reader:
				#print row[ Character name ],character
				if row[ Character name ] == character[ Name ]:
					for obj_char in objective_characteristics:
						if row[obj_char] != "NULL":
							char_objective[objective_characteristics.index(obj_char)] = row[obj_char]

		#print "\n"
		spamwriter.writerow([character["Name"]]+char_personality+char_objective)
		#pprint(character["Characteristics"])

	#print len(used_personalities),"/",len(personalities)
