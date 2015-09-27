
from xml.dom.minidom import Document, parseString
#from __future__ import print_function, division
from collections import Counter
    
import nltk, re, pprint
from nltk import word_tokenize
    
filenum_list = [7, 8, 9, 16, 17, 18, 25, 26, 27];        

noun_to_check = [ "art", "authority", "bar", "bum", "chair", "channel", 
    "child", "church", "circuit", "day", "detention", "dyke", "fatigue", "feeling", 
    "grip", "hearth", "holiday", "lady", "material", "mouth", "nation",  "nature", "restraint", "sense", "spade",
    "stress", "yew" ]

verb_to_check = [ "begin", "call", "carry", "collaborate", "develop", "draw", "dress", "drift", "drive", "face",  "find", "keep", "leave", "live",  "match", 
    "play", "post", "pull", "replace", "see", "serve", "strike", "train", "treat", "turn", "use", "wander", "wash", 
    "work" ]

adj_to_check = [ "blind", "faithful", "colourless", "cool", "fine", "fit", "free", "graceful", "green", "local", "natural", "oblique", "simple", "solemn",  
    "vital" ]

others_to_check = [ "empty" ]

# file5 = open( "total_pos.txt", "w")

for round in range(0, len(filenum_list)):
# for round in range(0, 1):
    filename = 'reconcile/Blog ' + str(filenum_list[round]) + '_eadsit_reconciled.xml'
    filename_alone = filename.rsplit('.', 1)[0]
    reconcile_file = open(filename, 'r')


    raw_file = open('raw/Blog ' + str(filenum_list[round]) + '.xml', 'r')
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



# for round in range(0, len(filenum_list)):
for round in range(0, 1):
    raw_file = open('raw/Blog ' + str(filenum_list[round]) + '.xml', 'r')
    # filename = 'reconcile/Blog ' + str(filenum_list[round]) + '_eadsit_reconciled.xml'
    # filename_alone = filename.rsplit('.', 1)[0]
    # reconcile_file = open(filename, 'r')
    sentences = str(raw_file.readlines())
    file2 = open( 'count/Blog ' + str(filenum_list[round]) + "_pos_complete_raw.txt", "w")
    tagged = nltk.sent_tokenize(sentences.strip())
    tagged = [nltk.word_tokenize(sent) for sent in tagged]
    tagged = [nltk.pos_tag(sent) for sent in tagged]

    i = 0
    noun_id = 0
    for tag in tagged:
        j = 0
        #    print tag[0]
        while True:
            if j >= len(tag):
                break
            file2.write(str(i)+","+str(j))
            file2.write("\n")
            temp_str = str(tag[j])
            file2.write(temp_str)
            file2.write("\n")
            temp_indicate = tag[j][0]
            
           
            j += 1
        i += 1

















