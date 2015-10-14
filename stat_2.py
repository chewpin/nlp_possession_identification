
from xml.dom.minidom import Document, parseString
#from __future__ import print_function, division
from collections import Counter, defaultdict
import operator
import nltk, re, pprint
from nltk import word_tokenize
import re
 
file_error = open( "stat_2/error.txt", "w")
file_total_object = open( "stat_2/total_object.txt", "w")
filenum_list = [1,2,3,4,5,6,7, 8, 9,10,11,12,13,14,15, 16, 17, 18,19,20,21,22,23,24, 25, 26, 27];
total_object_count = 0
total_object_end_tag_count = 0

agreement_total_count = 0
agreement_golden_total = agreement_silver_total = 0
file_golden_total = open( "stat_2/3+.txt", "w")
file_silver_total = open( "stat_2/2+.txt", "w")
file_regular_total = open( "stat_2/1+.txt", "w")

for round in range(0, len(filenum_list)):
# for round in range(0, 1):
    filename = 'Blog ' + str(filenum_list[round]) + '_reconciled.xml'
    # filename = 'Blog 22_reconciled.xml'
    file_golden_tag_only = open( "stat_2/golden/golden_tag_only_" + str(filenum_list[round]) + ".txt", "w")
    file_silver_tag_only = open( "stat_2/silver/golden_silver_tag_only_" + str(filenum_list[round]) + ".txt", "w")
    file = open("reconcile/" + filename, 'r')
    to_write_corpus_list_golden = []
    to_write_corpus_list_silver = []
    to_write_corpus_list_regular = []
    round_agreement_total_count = round_agreement_golden_total = round_agreement_silver_total = 0
    
    corpus = file.readlines()
    print "blog_id: ", filenum_list[round] ,"\n"
    file_golden_total.write("\n\nblog_id: " + str(filenum_list[round])+ "\n")
    file_silver_total.write("\n\nblog_id: " + str(filenum_list[round])+ "\n")
    file_regular_total.write("\n\nblog_id: " + str(filenum_list[round])+ "\n")
    sentence_num = 0
    for sentence in corpus:
        to_write_corpus_list_golden.append("")
        to_write_corpus_list_silver.append("")
        to_write_corpus_list_regular.append("")
        j = 0
        words = sentence.split()

        while True and j < len(words):
            temp_indicate = words[j]
            if temp_indicate != "<object":
                if "</object>" not in temp_indicate:
                    to_write_corpus_list_golden[sentence_num] += temp_indicate + " "
                    to_write_corpus_list_silver[sentence_num] += temp_indicate + " "
                    to_write_corpus_list_regular[sentence_num] += temp_indicate + " "
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
                                print "\n\nagreement_value: ", searchObj.group(1)
                                agreement_present = True
                                agreement_value = str(searchObj.group(1))
                                agreement_total_count += 1
                                round_agreement_total_count += 1
                                if len(agreement_value) == 3:
                                    golden  = True
                                    agreement_golden_total += 1
                                    print "GOLD"
                                    round_agreement_golden_total += 1
                                if len(agreement_value) >= 2:
                                    silver = True
                                    agreement_silver_total += 1
                                    round_agreement_silver_total += 1
                                    print "SILVER"
                            else:
                               print "Nothing found!!"
                            while find_in_tags_index < xml_end:
                                # print tag_sentence_str
                                if ">" in words[find_in_tags_index]:
                                    object_index_start = find_in_tags_index + 1
                                    object_index_end = find_in_tags_index + 1
                                    print "object start: ", words[find_in_tags_index]
                                    object_value = ""
                                    while "<" not in words[object_index_end]:
                                        print words[object_index_end]
                                        object_value += str(words[object_index_end]) + " "
                                        object_index_end += 1
                                    print "object value: ", object_value
                                find_in_tags_index += 1
                            file_total_object.write( str(total_object_count) + ": blog " + str(round) + "\t" + object_value + "\n" )
                            current_golden_sentence = ""
                            for sent in tag_sentence:
                                current_golden_sentence += sent + " "
                            current_silver_sentence = current_golden_sentence
                            current_regular_sentence = current_golden_sentence
                            # print current_golden_sentence
                            if not golden:
                                current_golden_sentence = re.sub('<object.*?/object>',object_value,current_golden_sentence, flags=re.DOTALL)
                            if not silver:
                                current_silver_sentence = re.sub('<object.*?/object>',object_value,current_silver_sentence, flags=re.DOTALL)
                            print current_golden_sentence
                            to_write_corpus_list_golden[sentence_num] += current_golden_sentence + " "
                            to_write_corpus_list_silver[sentence_num] += current_silver_sentence + " "
                            to_write_corpus_list_regular[sentence_num] += current_regular_sentence + " "
                        else: # wrong format, does not count
                            tag_sentence = words[xml_start:current_index]
                            current_golden_sentence = current_silver_sentence = current_regular_sentence = ""
                            for sent in tag_sentence:
                                current_golden_sentence += sent + " "
                            current_golden_sentence = re.sub('<object.*?>','',current_golden_sentence, flags=re.DOTALL)
                            to_write_corpus_list_golden[sentence_num] += current_golden_sentence + " "
                            to_write_corpus_list_silver[sentence_num] += current_golden_sentence + " "
                            to_write_corpus_list_regular[sentence_num] += current_golden_sentence + " "
                        j = current_index - 1
                        break
            j += 1
            # print "j = ", j, ", sent: ", to_write_corpus_list_golden[sentence_num] 
        # print "sentence_num = ", sentence_num, ", ", to_write_corpus_list_golden[sentence_num],  "\n\n\n"
        file_golden_tag_only.write(to_write_corpus_list_golden[sentence_num] + "\n")
        file_silver_tag_only.write(to_write_corpus_list_silver[sentence_num] + "\n")
        file_golden_total.write(to_write_corpus_list_golden[sentence_num] + "\n")
        file_silver_total.write(to_write_corpus_list_silver[sentence_num] + "\n")
        file_regular_total.write(to_write_corpus_list_regular[sentence_num] + "\n")
        sentence_num += 1


    print "total_object_count: ", total_object_count
    print "total_object_end_tag_count: ", total_object_end_tag_count
    # file_golden_tag_only.write( "\nobject num: " + str(round_agreement_total_count) + "\n" )
    # file_golden_tag_only.write( "golden object num: " + str(round_agreement_golden_total) + "\n" )
    # file_golden_tag_only.write( "silver+golden object num: " + str(round_agreement_silver_total)+ "\n"  )
    # file_golden_tag_only.write( "real silver object num: " + str(round_agreement_silver_total - round_agreement_golden_total)+ "\n"  )
file_golden_tag_only.close()
file_silver_tag_only.close()
file_total_object.write( "\nobject num: " + str(total_object_count) + "\n" )
file_total_object.write( "golden object num: " + str(agreement_golden_total) + "\n" )
file_total_object.write( "silver+golden object num: " + str(agreement_silver_total)+ "\n"  )
file_total_object.write( "real silver object num: " + str(agreement_silver_total - agreement_golden_total)+ "\n"  )
file_total_object.close()
file_error.close()
file_golden_total.close()
file_silver_total.close()
file_regular_total.close()
print "agreement_total_count: ", agreement_total_count
print "agreement_golden_count: ", agreement_golden_total
print "agreement_silver_count: ", agreement_silver_total
print "agreement pure silver: ", agreement_silver_total - agreement_golden_total
print "agreement pure regular: ", agreement_total_count - agreement_silver_total
































