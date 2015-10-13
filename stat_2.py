
from xml.dom.minidom import Document, parseString
#from __future__ import print_function, division
from collections import Counter, defaultdict
import operator
import nltk, re, pprint
from nltk import word_tokenize
import re
 
file_error = open( "stat_2/error.txt", "w")
filenum_list = [1,2,3,4,5,6,7, 8, 9,10,11,12,13,14,15, 16, 17, 18,19,20,21,22,23,24, 25, 26, 27];
total_object_count = 0
total_object_end_tag_count = 0

to_write_corpus_list = []



# for round in range(0, len(filenum_list)):
for round in range(0, 1):
    # filename = 'Blog ' + str(filenum_list[round]) + '_reconciled.xml'
    filename = 'Blog 14_reconciled.xml'
    file_golden_tag_only = open( "stat_2/golden/golden_tag_only_" + str(filenum_list[round]) + ".txt", "w")
    file_golden_silver_tag_only = open( "stat_2/silver/golden_silver_tag_only_" + str(filenum_list[round]) + ".txt", "w")
    file = open("reconcile/" + filename, 'r')
    
    corpus = file.readlines()
    # sentences = sentences.split()
    print "blog_id: ", filenum_list[round] ,"\n"
    sentence_num = 0
    for sentence in corpus:
        to_write_corpus_list.append("")
        j = 0
        # file_golden_tag_only.write(sentence)
        # print sentence
        words = sentence.split()

        while True and j < len(words):
            temp_indicate = words[j]
            # file_error.write( "\n" + temp_indicate)
            if temp_indicate != "<object":
                if "</object>" not in temp_indicate:
                    to_write_corpus_list[sentence_num] += temp_indicate + " "
            else:
                xml_start = j
                xml_end = -1
                value_pos_temp = []
                object_pos_temp = []
                value_value = value_pos = ""
                object_value = object_pos = ""
                status_value = agreement_value = type_value = ""
                object_index_start = object_index_end = 0
                agreement_index = 0
                status_index = 0
                type_index = 0
                id_index = 0
                value_index_start = value_index_end = 0
                agreement_present = type_present = status_present = False
                golden = False

                current_index = j
                # file_error.write( "\t" + temp_indicate )
                while True and current_index < len(words):
                    # print current_index
                    current_index += 1
                    temp_indicate = words[current_index]
                    if "</object>" in temp_indicate or "<object" in temp_indicate:
                        if "</object>" in temp_indicate: # needs end tag
                            total_object_count += 1
                            # print temp_indicate
                            xml_end = current_index
                            total_object_end_tag_count += 1
                            file_error.write( str(total_object_count) + str(words[xml_start:xml_end+1]) + "\n")
                            tag_sentence = words[xml_start:xml_end+1]
                            current_golden_sentence = ""
                            for sent in tag_sentence:
                                current_golden_sentence += sent + " "
                            # print current_golden_sentence
                            current_golden_sentence = re.sub('<object.*?/object>','',current_golden_sentence, flags=re.DOTALL)
                            print current_golden_sentence
                            to_write_corpus_list[sentence_num] += current_golden_sentence + " "
                        else:
                            tag_sentence = words[xml_start:current_index]
                            current_golden_sentence = ""
                            for sent in tag_sentence:
                                current_golden_sentence += sent + " "
                            current_golden_sentence = re.sub('<object.*?>','',current_golden_sentence, flags=re.DOTALL)
                            to_write_corpus_list[sentence_num] += current_golden_sentence + " "
                        j = current_index - 1
                        break
            j += 1
        file_golden_tag_only.write(to_write_corpus_list[sentence_num] + "\n")
        sentence_num += 1


    print "total_object_count: ", total_object_count
    print "total_object_end_tag_count: ", total_object_end_tag_count
file_golden_tag_only.close()
file_golden_silver_tag_only.close()
file_error.close()
































