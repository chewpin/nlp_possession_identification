# for feature 151027
from xml.dom.minidom import Document, parseString
#from __future__ import print_function, division
from collections import Counter, defaultdict
import operator
import nltk, re, pprint
from nltk import word_tokenize
import re
 
read_word_category_dict = {}
read_word_category_enum_dict = set()
file_read_word_category_dict = open('category/stat/word_category_man.txt', 'r')
sentences = file_read_word_category_dict.readlines()
index = 0
read_object = ""
read_category = ""
read_word_category_dict = {}
for sentence in sentences:
    sentence = sentence.rstrip('\n')
    if index % 2 == 1:
        read_category = sentence.strip()
        if "/" in read_category:
            read_category = str(read_category.split("/",1)[0])
        read_word_category_dict[read_object] = read_category
    else:
        read_object = sentence.strip()
    index += 1
sorted_read_word_category_dict = sorted(read_word_category_dict.items(), key=operator.itemgetter(1))
for i in range(0,len(sorted_read_word_category_dict)):
    print sorted_read_word_category_dict[i][1] , ":  " , sorted_read_word_category_dict[i][0]
file_read_word_category_dict.close()



file_error = open( "feature_1/error.txt", "w")
filenum_list = [1,2,3,4,5,6,7, 8, 9,10,11,12,13,14,15, 16, 17, 18,19,20,21,22,23,24, 25, 26, 27]

clean_tag_total_object_count = 0
has_category_object_count = 0




for round in range(0, len(filenum_list)):
# for round in range(0, 1):
    filename = 'Blog ' + str(filenum_list[round]) + '_reconciled.xml'
    file_clean = open( "reconcile/clean/" + str(filenum_list[round]) + "_clean.txt", "r" )
    file_clean_index = open( "reconcile/clean/" + str(filenum_list[round]) + "_clean_index.txt", "r" )
    file = open("reconcile/" + filename, 'r')

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
        j = 0
        words = sentence.split()
        clean_words = clean_sentence.split()
        get_clean_tag_map_count_word = 0
        get_clean_tag_map_count_clean = 0
        clean_tag_map = {}
        clean_index_corpus_content = clean_index_corpus_content.split()
        temp_index = 0

        # print clean_words
        clean_sentence = clean_sentence.decode('utf-8')
        clean_words = clean_sentence.split()
        tagged = nltk.pos_tag(clean_words)
        # print "\n\n\n1111111: ", tagged
        words = tagged
        while temp_index < len(clean_index_corpus_content):
            object_value = ""
            value_value = ""
            if clean_index_corpus_content[temp_index] != clean_index_corpus_content[temp_index+1]:
                # print clean_words[int(clean_index_corpus_content[temp_index]):int(clean_index_corpus_content[temp_index+1])+1]
                clean_tag_total_object_count += 1
                for temp_i in range(int(clean_index_corpus_content[temp_index]),int(clean_index_corpus_content[temp_index+1])+1):
                    print tagged[ temp_i ][0], ", ", tagged[ temp_i ][1]
                    object_value += tagged[ temp_i ][0] + " "

            else:
                clean_tag_total_object_count += 1
                # print clean_words[int(clean_index_corpus_content[temp_index])]
                print tagged[ int(clean_index_corpus_content[temp_index]) ][0], ", ", tagged[ int(clean_index_corpus_content[temp_index]) ][1]
                object_value += tagged[ int(clean_index_corpus_content[temp_index]) ][0]
            temp_index += 2
            object_value_value_value_len = int(clean_index_corpus_content[temp_index])
            for i in range(0,object_value_value_value_len):
                temp_index += 1
                value_value += clean_index_corpus_content[temp_index] + " "
            temp_index += 1
            print value_value
            value_value = value_value.strip()
            object_value = object_value.strip()
            # print "             ",  object_value

            if value_value in read_word_category_dict:
                # print object_value, " category: ", read_word_category_dict[object_value]
                has_category_object_count += 1
                # read_word_category_enum_dict.add(read_word_category_dict[value_value])
                # if blog_dict["category"][round] not in category_dict:
                #     category_dict[ blog_dict["category"][round] ] = {}
                #     if 'word_category' not in category_dict[ blog_dict["category"][round] ]:
                #         category_dict[ blog_dict["category"][round] ]['word_category'] = {}
                #         category_dict[ blog_dict["category"][round] ]['word_category'][read_word_category_dict[value_value]] = 1
                # else:
                #     if 'word_category' not in category_dict[ blog_dict["category"][round] ]:
                #         category_dict[ blog_dict["category"][round] ]['word_category'] = {}
                #         category_dict[ blog_dict["category"][round] ]['word_category'][read_word_category_dict[value_value]] = 1
                #     else:
                #         if read_word_category_dict[value_value] in category_dict[ blog_dict["category"][round] ]['word_category']:
                #             category_dict[ blog_dict["category"][round] ]['word_category'][read_word_category_dict[value_value]] += 1
                #         else:
                #             category_dict[ blog_dict["category"][round] ]['word_category'][read_word_category_dict[value_value]] = 1
            else:
                print "not category: ", value_value
        sentence_num += 1
    # file_clean.close()

    print "clean_tag_total_object_count: ", clean_tag_total_object_count
    print "has_category_object_count: ", has_category_object_count
file_error.close()
































