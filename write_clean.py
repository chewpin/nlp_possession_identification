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
# file_golden_total = open( "feature_1/3+.txt", "w")
# file_silver_total = open( "feature_1/2+.txt", "w")
# file_regular_total = open( "feature_1/1+.txt", "w")



# for round in range(0, len(filenum_list)):
for round in range(0, 1):
    filename = 'Blog ' + str(filenum_list[round]) + '_reconciled.xml'
    file_clean = open( "reconcile/clean/" + str(filenum_list[round]) + "_clean.txt", "w" )
    file_clean_index = open( "reconcile/clean/" + str(filenum_list[round]) + "_clean_index.txt", "w" )
    # filename = 'Blog 22_reconciled.xml'
    # file_golden_tag_only = open( "feature_1/golden/golden_tag_only_" + str(filenum_list[round]) + ".txt", "w")
    # file_silver_tag_only = open( "feature_1/silver/golden_silver_tag_only_" + str(filenum_list[round]) + ".txt", "w")
    file = open("reconcile/" + filename, 'r')
    # to_write_corpus_list_golden = []
    # to_write_corpus_list_silver = []
    # to_write_corpus_list_regular = []
    to_write_corpus_list_clean = []
    round_agreement_total_count = round_agreement_golden_total = round_agreement_silver_total = 0
    
    corpus = file.readlines()
    print "blog_id: ", filenum_list[round] ,"\n"
    # file_golden_total.write("\n\nblog_id: " + str(filenum_list[round])+ "\n")
    # file_silver_total.write("\n\nblog_id: " + str(filenum_list[round])+ "\n")
    # file_regular_total.write("\n\nblog_id: " + str(filenum_list[round])+ "\n")
    sentence_num = 0
    for sentence in corpus:
        clean_object_location = {}
        clean_file_index = 0
        # to_write_corpus_list_golden.append("")
        # to_write_corpus_list_silver.append("")
        # to_write_corpus_list_regular.append("")
        to_write_corpus_list_clean.append("")
        j = 0
        sentence = sentence.replace(",", " , ")
        sentence = sentence.replace(".", " . ")
        sentence = sentence.replace("?", " ? ")
        sentence = sentence.replace(";", " ; ")
        sentence = sentence.replace(":", " : ")
        sentence = sentence.replace("!", " ! ")
        sentence = sentence.replace("=", " = ")
        sentence = sentence.replace("+", " + ")
        sentence = sentence.replace("$", " $ ")
        sentence = sentence.replace("%", " % ")
        sentence = sentence.replace(")", " ) ")
        sentence = sentence.replace("(", " ( ")
        sentence = sentence.replace("}", " } ")
        sentence = sentence.replace("{", " { ")
        sentence = sentence.replace("]", " ] ")
        sentence = sentence.replace("[", " [ ")
        sentence = sentence.replace('"', '  "  ')
        sentence = re.sub( r'([a-zA-Z])([!@#$%^*(){};:,\\.?\|`~=_+])', r'\1 \2', sentence)
        words = sentence.split()
        print sentence

        while True and j < len(words):
            temp_indicate = words[j]
            if temp_indicate != "<object":
                if "</object>" not in temp_indicate:
                    temp_indicate = temp_indicate
                    to_write_corpus_list_clean[sentence_num] += temp_indicate + " "
                    # print clean_file_index, ": ", temp_indicate
                    clean_file_index += 1
                    # to_write_corpus_list_golden[sentence_num] += temp_indicate + " "
                    # to_write_corpus_list_silver[sentence_num] += temp_indicate + " "
                    # to_write_corpus_list_regular[sentence_num] += temp_indicate + " "
            else:
                xml_start = j
                xml_end = -1
                value_value = ""
                object_value = ""
                agreement_value = ""
                object_index_start = object_index_end = value_index = 0
                agreement_present = final = False
                golden = silver = False

                current_index = j
                while True and current_index < len(words):
                    # print current_index
                    current_index += 1
                    temp_indicate = words[current_index]
                    if "</object>" in temp_indicate or "<object" in temp_indicate:
                        if "</object>" in temp_indicate: # needs end tag
                            # print temp_indicate
                            xml_end = current_index
                            file_error.write( str(total_object_count) + str(words[xml_start:xml_end+1]) + "\n")
                            tag_sentence = words[xml_start:xml_end+1]
                            tag_sentence_str = ""
                            for sent in tag_sentence:
                                tag_sentence_str += sent + " "
                            find_in_tags_index = xml_start
                            searchObj = re.search( r'value *= *"(.*)" id *', tag_sentence_str, re.I+re.S)
                            if searchObj:
                                value_value = str(searchObj.group(1)).strip()
                                value_value_list = value_value.split()
                                print "value_value: ", value_value
                                print value_value_list
                            else:
                               print "Nothing found!!"
                            searchObj = re.search( 'agreement *= *"(.*)" *>.*<.*>', tag_sentence_str, re.M|re.I)
                            if searchObj:
                                # print "\n\nagreement_value: ", searchObj.group(1)
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
                            searchObj = re.search( 'status *= *"(.*)" *>.*<.*>', tag_sentence_str, re.M|re.I)
                            if searchObj:
                                # print "\n\nagreement_value: ", searchObj.group(1)
                                final = True
                                print "             FINAL!!!"
                            else:
                               print "NOT FINAL!!"
                            if final:
                                total_object_count += 1
                                total_object_end_tag_count += 1
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
                                
                                clean_sentence = re.sub('<object.*?/object>',object_value,tag_sentence_str, flags=re.DOTALL)
                                clean_sentence = clean_sentence.strip()
                                to_write_corpus_list_clean[sentence_num] += clean_sentence + " "
                                temp_strip_clean = clean_sentence.split()
                                temp_clean_size = 0
                                for temp in temp_strip_clean:
                                    temp_clean_size += 1
                                    print clean_file_index, ": ", temp
                                    clean_file_index += 1
                                file_clean_index.write( str(clean_file_index-temp_clean_size) + " " + str(clean_file_index-1) + " " + str(len(value_value_list)) + " ")
                                for i in range(0,len(value_value_list)):
                                    file_clean_index.write(str(value_value_list[i]) + " ")


                        j = current_index - 1
                        break # END if "</object>" in temp_indicate:
            j += 1
            # print "j = ", j, ", sent: ", to_write_corpus_list_golden[sentence_num] 
        # print "clean_sentence: ", to_write_corpus_list_clean[sentence_num]
        # print "sentence_num = ", sentence_num, ", ", words,  "\n\n"
        file_clean.write(to_write_corpus_list_clean[sentence_num] + "\n")
        file_clean_index.write( "\n" )
        # file_golden_tag_only.write(to_write_corpus_list_golden[sentence_num] + "\n")
        # file_silver_tag_only.write(to_write_corpus_list_silver[sentence_num] + "\n")
        # file_golden_total.write(to_write_corpus_list_golden[sentence_num] + "\n")
        # file_silver_total.write(to_write_corpus_list_silver[sentence_num] + "\n")
        # file_regular_total.write(to_write_corpus_list_regular[sentence_num] + "\n")
        sentence_num += 1
        print "\n\n\n"
        #  END while True and j < len(words):
    file_clean.close()

    print "total_object_count: ", total_object_count
    print "total_object_end_tag_count: ", total_object_end_tag_count
    # file_golden_tag_only.write( "\nobject num: " + str(round_agreement_total_count) + "\n" )
    # file_golden_tag_only.write( "golden object num: " + str(round_agreement_golden_total) + "\n" )
    # file_golden_tag_only.write( "silver+golden object num: " + str(round_agreement_silver_total)+ "\n"  )
    # file_golden_tag_only.write( "real silver object num: " + str(round_agreement_silver_total - round_agreement_golden_total)+ "\n"  )
# file_golden_tag_only.close()
# file_silver_tag_only.close()
file_total_object.write( "\nobject num: " + str(total_object_count) + "\n" )
# file_total_object.write( "golden object num: " + str(agreement_golden_total) + "\n" )
# file_total_object.write( "silver+golden object num: " + str(agreement_silver_total)+ "\n"  )
# file_total_object.write( "real silver object num: " + str(agreement_silver_total - agreement_golden_total)+ "\n"  )
file_total_object.close()
file_error.close()
# file_golden_total.close()
# file_silver_total.close()
# file_regular_total.close()
print "agreement_total_count: ", agreement_total_count
# print "agreement_golden_count: ", agreement_golden_total
# print "agreement_silver_count: ", agreement_silver_total
# print "agreement pure silver: ", agreement_silver_total - agreement_golden_total
# print "agreement pure regular: ", agreement_total_count - agreement_silver_total
































