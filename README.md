GoT
===

1. DataGen/extractSubjective.py : Extract subjective features of all characters and dump them in a file called subjectiveFeatures.json

2. DataGen/analyseSubjective.py : From the subjectiveFeatures.json dumped by  extractSubjective.py extract physical features and personality traits for each characters

3. DataGen/get_personalities : Cleans data from the file /Data/traits1.txt and /Data/traits2.txt by removing duplicates.

3. DataGen/getObjectiveFeatures.py : a> Scrap data about all characters specified in the file Data/character_names.txt by visiting all online wiki pages of each characters and extract objective features for every characters. 
   b> Read objective features from a structured data set from the file Data/character_attributes.csv
   c> Combine objective features obtained from steps (a) and (b) and dump them to stderr in csv format.

  A csv file containing objective features can be generated using the command
  python getObjectiveFeatures.py 2> file_name.csv	

4. DataGen/get_occupations.py : Extract from data in the file Data/status.csv and extract a list of all occupations.

5. DataGen/get_occupations.py : Extract a list of all occupations from the file Data/status.csv



Part 2 : Visualizations
============================

The visualizations are implemented using d3 in the Viz directory. To open a visulaization, start any http server with Viz as root directory. SimpleHTTPServer can be used to view d3 visualizations. Once the server is started, the visualzations can be viewed by opening theit html files from ay javascript enabled browser



