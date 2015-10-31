# for feature 151027
from xml.dom.minidom import Document, parseString
#from __future__ import print_function, division
from collections import Counter, defaultdict
import operator
import nltk, re, pprint
from nltk import word_tokenize
import re
 
file_error = open( "feature_1/error.txt", "w")
filenum_list = [1,2,3,4,5,6,7, 8, 9,10,11,12,13,14,15, 16, 17, 18,19,20,21,22,23,24, 25, 26, 27]

clean_tag_total_object_count = 0


for round in range(0, len(filenum_list)):
# for round in range(0, 1):
    filename = 'Blog ' + str(filenum_list[round]) + '_reconciled.xml'
    file_clean = open( "reconcile/clean/" + str(filenum_list[round]) + "_clean.txt", "r" )
    file_clean_index = open( "reconcile/clean/" + str(filenum_list[round]) + "_clean_index.txt", "r" )
    file = open("reconcile/" + filename, 'r')
    # to_write_corpus_list_clean = []
    round_agreement_total_count = round_agreement_golden_total = round_agreement_silver_total = 0
    
    corpus = file.readlines()
    clean_corpus = file_clean.readlines()
    print "blog_id: ", filenum_list[round] ,"\n"
    sentence_num = 0
    clean_index_corpus = file_clean_index.readlines()
    corpus_str = str(corpus)

    for sentence in corpus:
        clean_sentence = clean_corpus[sentence_num]
        clean_index_corpus_content = clean_index_corpus[sentence_num]
        # print clean_sentence
        # to_write_corpus_list_clean.append("")
        j = 0
        words = sentence.split()
        clean_words = clean_sentence.split()
        get_clean_tag_map_count_word = 0
        get_clean_tag_map_count_clean = 0
        clean_tag_map = {}
        clean_index_corpus_content = clean_index_corpus_content.split()
        # print clean_index_corpus_content
        temp_index = 0

        # print clean_words
        clean_sentence = clean_sentence.decode('utf-8')
        clean_words = clean_sentence.split()
        tagged = nltk.pos_tag(clean_words)
        # print "\n\n\n1111111: ", tagged
        words = tagged
        while temp_index < len(clean_index_corpus_content):
            if clean_index_corpus_content[temp_index] != clean_index_corpus_content[temp_index+1]:
                # print clean_words[int(clean_index_corpus_content[temp_index]):int(clean_index_corpus_content[temp_index+1])+1]
                clean_tag_total_object_count += 1
                for temp_i in range(int(clean_index_corpus_content[temp_index]),int(clean_index_corpus_content[temp_index+1])+1):
                    print tagged[ temp_i ][0], ", ", tagged[ temp_i ][1]

            else:
                clean_tag_total_object_count += 1
                # print clean_words[int(clean_index_corpus_content[temp_index])]
                print tagged[ int(clean_index_corpus_content[temp_index]) ][0], ", ", tagged[ int(clean_index_corpus_content[temp_index]) ][1]
            temp_index += 2
        

        
        # print "clean_sentence: ", to_write_corpus_list_clean[sentence_num]
        # print "sentence_num = ", sentence_num, ", ", sentence,  "\n\n"
        # file_clean.write(to_write_corpus_list_clean[sentence_num] + "\n")
        sentence_num += 1
    # file_clean.close()

    print "clean_tag_total_object_count: ", clean_tag_total_object_count
file_error.close()
































