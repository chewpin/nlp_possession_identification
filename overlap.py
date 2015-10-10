from xml.dom.minidom import Document, parseString
#from __future__ import print_function, division
from collections import Counter
    
import nltk, re, pprint
from nltk import word_tokenize


file6 = open( "stat/result_transformed.html", "w")
result = ""

with open ("stat/results.html", "r") as file:
    data=file.read().replace('\n', '')
    print data
    result = data.replace("\"", "\\\"")
    
file6.write(result)
file.close()
file6.close()