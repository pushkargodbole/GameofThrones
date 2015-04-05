import urllib2
import json
import time
import os
from nltk import PorterStemmer
from get_characters import get_characters
from get_personalities import get_personalities
from pattern.en import parsetree
import nltk
from collections import Counter

url_base = "http://awoiaf.westeros.org/api.php?format=json&action=query&titles="
url_end = "&prop=revisions&rvprop=content"
characters = get_characters("../Data/awoiaf_loc.txt")
personalities = get_personalities(['../Data/traits1.txt', '../Data/traits2.txt'])
personality_stems = []
for personality in personalities:
	personality_stems.append(str(PorterStemmer().stem_word(personality).lower()))
	#print personality, str(PorterStemmer().stem_word(personality).lower())

physical_features = ['hair','eyes','face','beard','skin','flesh', 'accent', 'nose','legs', 'shoulders','stomach','jaw','ears','nipples','laugh','smile','lips','cheekbones','height','chin','mustache','scales','build','voice','eyebrows','appetite','chest','grasp','temper','figure','hairs','tongue','mouth']
final_data = {'Type': 'Subjective features', 'Characters':[]}

abstract_word_list = []

for name in characters:#[0:500]:
	print name
	char_dict = {'Name': name, 'Appearance':{}, 'Characteristics':{}}
	final_data_names = []
	url = url_base+name+url_end
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
	json_obj = urllib2.urlopen(req)
	json_data = json.load(json_obj)
	data = str(json_data["query"]["pages"])
	start = data.find("Appearance and Character==")
	if start == -1:
		start = data.find("==Appearance")
	if start == -1:
		start = data.find("Character==")	
	end = data[start:].find("\\n\\n==")
	#print start,end
	if start != -1:
		#print data[start:start+end]
		ACdata = data[start:start+end]
		ACphysical_list = []
		ACstem_list = []
		sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
		sent_list = sent_detector.tokenize(ACdata.strip())
		for sent in sent_list:
			tree = parsetree(sent)
			sent_tok = nltk.word_tokenize(sent)
			tag_list = nltk.pos_tag(sent_tok)
			for pair in tag_list:
				if pair[1] == 'JJ':# or pair[0] in ['cold','melancholy']:
					for sentence in tree:
						for chunk in sentence.chunks:
							if pair[0] in chunk.string:
								flag = 0
								for word in chunk:
									if word.tag == 'NN' or word.tag == 'NNS':
										#if the noun is a physical feature
										if word.string in physical_features:
											ACphysical_list.append(pair[0].lower()+' '+word.string.lower())

										#there should be no subject nouns in the chunk other than the following list	
										if word.string not in ['woman', 'man', 'mind', 'heart', 'body', 'fighter', 'warrior', 'features', 'lifestyle','soldier','girl','boy','youth','knight','appearance','graces','leader','temperament','lad']+physical_features:
											flag = 1
											if word.string != 'Appearance' and 'ref' not in word.string.lower():
												abstract_word_list.append(word)
												#print chunk.words

									#there should be no negation indicators in the chunk like the following list
									if word.string.lower() in ['no','not','none','nobody','nothing','neither','nowhere','never','hardly','scarcely','barely']:
										flag = 1
										print "Negation found !!!!",word.string
										if word.string != 'Appearance' and 'ref' not in word.string.lower():
											abstract_word_list.append(word)
											#print chunk.words
											
								if flag == 0:		
									ACstem_list.append(str(PorterStemmer().stem_word(pair[0])))			

		for word in ACstem_list:
			if word in personality_stems:
				#print word
				#char_dict = {'Name': name, 'Appearance':{}, 'Characteristics':{}}
				if personalities[personality_stems.index(word)] not in char_dict['Characteristics']:
					char_dict['Characteristics'][personalities[personality_stems.index(word)]] = 1
				else:
					char_dict['Characteristics'][personalities[personality_stems.index(word)]] += 1
				
		for physical_feature in ACphysical_list:

			#char_dict = {'Name': name, 'Appearance':{}, 'Characteristics':{}}
			if physical_feature not in char_dict['Appearance']:
				char_dict['Appearance'][physical_feature] = 1
			else:
				char_dict['Appearance'][physical_feature] += 1
				
		final_data['Characters'].append(char_dict)

#print json.dumps(final_data, sort_keys=True,indent=4, separators=(',', ': '))

with open('subjectiveFeatures.json', 'w') as outfile:
    json.dump(final_data, outfile)

#for x,y in Counter(abstract_word_list).items():
#	print x,y





