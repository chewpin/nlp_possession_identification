
from xml.dom.minidom import Document, parseString
#from __future__ import print_function, division
from collections import Counter
    
import nltk, re, pprint
from nltk import word_tokenize
  
    filename = 'picturable_words.txt'
    filename_alone = filename.rsplit('.', 1)[0]
    reconcile_file = open(filename, 'r')


    raw_file = open('picturable.txt', 'r')
    raw_sentences = raw_file.readlines()
    for raw_sentence in raw_sentences:
        raw_words = raw_sentence.split()
        # print raw_words
    print "\n\n\n"
    reconcile_sentences = reconcile_file.readlines()
    for reconcile_sentence in reconcile_sentences:
        # print reconcile_sentence
        reconcile_words = reconcile_sentence.split()
        # print reconcile_words

        raw_i = i = 0
        # print "reconcile_words length: " , len(reconcile_words), "\n"
        while i < len(reconcile_words):
            # print str(i) + ": " , reconcile_words[i]
            while i < len(reconcile_words) and reconcile_words[i] != "<object" :
                # print str(i) + ": " , reconcile_words[i] , " != <object"
                i += 1
                raw_i += 1
            if i >= len(reconcile_words):
                break
            while  i < len(reconcile_words) and ">" not in reconcile_words[i]:
                # print str(i) + ": " , reconcile_words[i] , " != e>"
                i += 1
            if i >= len(reconcile_words):
                break
            i += 1
            # while i < len(reconcile_words) and reconcile_words[i] != '</object>' and reconcile_words[i] != '</object>,' and reconcile_words[i] != '</object>.':
            while i < len(reconcile_words) and "</object>" not in reconcile_words[i]:
                # if i == current_index:
                    # clean_index = raw_i
                print "object: " , reconcile_words[i]
                raw_i += 1
                i += 1
                # print str(i) + ": " , reconcile_words[i]
            print "\n"
            if i >= len(reconcile_words):
                break   
    # raw_file.close()
    reconcile_file.close()
# file5.close()

















