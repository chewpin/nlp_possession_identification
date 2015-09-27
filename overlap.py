from xml.dom.minidom import Document, parseString
#from __future__ import print_function, division
from collections import Counter
    
import nltk, re, pprint
from nltk import word_tokenize

noun_to_check = [ "art", "authority", "bar", "bum", "chair", "channel", 
    "child",  "church", "circuit", "day", "detention", "dyke", "fatigue", "feeling", 
    "grip", "hearth", "holiday", "lady", "material", "mouth", "nation",  "nature", "restraint", "sense", "spade",
    "stress", "yew",      
    "children", "ladies"]

verb_to_check = [ "begin", "call", "carry", "collaborate", "develop", "draw", "dress", "drift", "drive", "face",  "find", "keep", "leave", "live",  "match", 
    "play", "post", "pull", "replace", "see", "serve", "strike", "train", "treat", "turn", "use", "wander", "wash", 
    "work",
    "began", "begun", "carried", "drew", "drove", "driven", "found", "kept", "left", "saw", "seen", "struck", "striken" ]

adj_to_check = [ "blind", "faithful", "colourless", "cool", "fine", "fit", "free", "graceful", "green", "local", "natural", "oblique", "simple", "solemn",  
    "vital" ]
file6 = open( "stat/overlap_object.txt", "w")
file = open("stat/total_object.txt", 'r')
sentences = str(file.readlines())

for noun in noun_to_check:
    if noun in sentences:
    	file6.write(noun + "\n") 

for verb in verb_to_check:
    if verb in sentences:
    	file6.write(verb + "\n") 

for adj in adj_to_check:
    if adj in sentences:
    	file6.write(adj + "\n") 
file.close()
file6.close()