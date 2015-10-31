# for feature 151027
from xml.dom.minidom import Document, parseString
#from __future__ import print_function, division
from collections import Counter, defaultdict
import operator
import nltk, re, pprint
from nltk import word_tokenize
import re
 
file_error = open( "feature_1/error.txt", "w")
file_total_object = open( "feature_1/total_object.txt", "w")
filenum_list = [1,2,3,4,5,6,7, 8, 9,10,11,12,13,14,15, 16, 17, 18,19,20,21,22,23,24, 25, 26, 27];
total_object_count = 0
total_object_end_tag_count = 0

agreement_total_count = 0
agreement_golden_total = agreement_silver_total = 0

# for round in range(0, len(filenum_list)):
for round in range(0, 1):
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

    # tagged = nltk.sent_tokenize(corpus_str.strip())
    # tagged = [nltk.word_tokenize(sent) for sent in tagged]
    # tagged = [nltk.pos_tag(sent) for sent in tagged]
    # print tagged

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
        # print "1111111: ", tagged

        while temp_index < len(clean_index_corpus_content):
            if clean_index_corpus_content[temp_index] != clean_index_corpus_content[temp_index+1]:
                # print clean_words[int(clean_index_corpus_content[temp_index]):int(clean_index_corpus_content[temp_index+1])+1]
                for temp_i in range(int(clean_index_corpus_content[temp_index]),int(clean_index_corpus_content[temp_index+1])+1):
                    print tagged[ temp_i ][0], ", ", tagged[ temp_i ][1]

            else:
                # print clean_words[int(clean_index_corpus_content[temp_index])]
                print tagged[ int(clean_index_corpus_content[temp_index]) ][0], ", ", tagged[ int(clean_index_corpus_content[temp_index]) ][1]
            temp_index += 2


        while True and j < len(words):
            temp_indicate = words[j]
            if temp_indicate != "<object":
                if "</object>" not in temp_indicate:
                    temp_indicate = temp_indicate
                    # to_write_corpus_list_clean[sentence_num] += temp_indicate + " "
            else:
                xml_start = j
                xml_end = -1
                value_value = ""
                object_value = ""
                agreement_value = ""
                object_index_start = object_index_end = 0
                agreement_present = False
                golden = silver = False

                current_index = j
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
                            tag_sentence_str = ""
                            for sent in tag_sentence:
                                tag_sentence_str += sent + " "
                            find_in_tags_index = xml_start
                            searchObj = re.search( 'agreement *= *"(.*)" *>.*<.*>', tag_sentence_str, re.M|re.I)
                            if searchObj:
                                # print "\n\nagreement_value: ", searchObj.group(1)
                                agreement_present = True
                                agreement_value = str(searchObj.group(1))
                                agreement_total_count += 1
                                round_agreement_total_count += 1
                                if len(agreement_value) == 3:
                                    golden  = True
                                    agreement_golden_total += 1
                                    # print "GOLD"
                                    round_agreement_golden_total += 1
                                if len(agreement_value) >= 2:
                                    silver = True
                                    agreement_silver_total += 1
                                    round_agreement_silver_total += 1
                                    # print "SILVER"
                            else:
                               print "Nothing found!!"
                            while find_in_tags_index < xml_end:
                                # print tag_sentence_str
                                if ">" in words[find_in_tags_index]:
                                    object_index_start = find_in_tags_index + 1
                                    object_index_end = find_in_tags_index + 1
                                    # print "object start: ", words[find_in_tags_index]
                                    object_value = ""
                                    while "<" not in words[object_index_end]:
                                        # print words[object_index_end]
                                        object_value += str(words[object_index_end]) + " "
                                        object_index_end += 1
                                    object_value = object_value.strip()
                                    # print "object value: [" + str(object_value) + "]"
                                find_in_tags_index += 1
                            file_total_object.write( str(total_object_count) + ": blog " + str(round) + "\t" + object_value + "\n" )
                            
                            # clean_sentence = re.sub('<object.*?/object>',object_value,tag_sentence_str, flags=re.DOTALL)
                            # clean_sentence = clean_sentence.strip()
                            # to_write_corpus_list_clean[sentence_num] += clean_sentence + " "
                        else: # wrong format, does not count
                            tag_sentence = words[xml_start:current_index]
                            tag_sentence_str = ""
                            for sent in tag_sentence:
                                tag_sentence_str += sent + " "
                            # clean_sentence = re.sub('<object.*?>','',tag_sentence_str, flags=re.DOTALL)
                            # clean_sentence = clean_sentence.strip()
                            # to_write_corpus_list_clean[sentence_num] += clean_sentence + " "
                            # print "INVALID\nINVALID\nINVALID\nINVALID\nINVALID\nINVALID\nINVALID\nINVALID\n"
                            # print clean_sentence
                        j = current_index - 1
                        break # END if "</object>" in temp_indicate:
            j += 1
            # print "j = ", j, ", sent: ", to_write_corpus_list_golden[sentence_num] 
        # print "clean_sentence: ", to_write_corpus_list_clean[sentence_num]
        # print "sentence_num = ", sentence_num, ", ", sentence,  "\n\n"
        # file_clean.write(to_write_corpus_list_clean[sentence_num] + "\n")
        sentence_num += 1
        # if sentence_num > 18:
        #     break
        #  END while True and j < len(words):
    # file_clean.close()

    print "total_object_count: ", total_object_count
    print "total_object_end_tag_count: ", total_object_end_tag_count
file_total_object.write( "\nobject num: " + str(total_object_count) + "\n" )
file_total_object.close()
file_error.close()
print "agreement_total_count: ", agreement_total_count
































