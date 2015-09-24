
from xml.dom.minidom import Document, parseString
#from __future__ import print_function, division
from collections import Counter
    
import nltk, re, pprint
from nltk import word_tokenize
    
filenum_list = [7, 8, 9, 16, 17, 18, 25, 26, 27];

# def get_index( sentence, current_index, clean_sentence ):
#     clean_sentence_index = 0
#     clean_index = 0
#     i = 0
#     clean_i = 0
#     while i < len(sentence):
#         if sentence[i][0] != "<":
#             i += 1
#             clean_i += 1
#         else:
#             while sentence[i][0] != ">":
#                 i += 1
#                 if i >= len(sentence):
#                     break
#             while sentence[i][0] != "<":
#                 if i == current_index:
#                     clean_index = clean_i
#                 clean_i += 1
#                 i += 1
#                 if i >= len(sentence):
#                     break
#             i += 2 # after /object >
#             if i >= len(sentence):
#                 break
#     print "clean sentence: " + clean_sentence
#     print "clean index: " + str(clean_index)
#     return clean_index
        


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




















# i = 0 # line_no
#     for tag in tagged:
#         j = 0
#         #    print tag[0]
#         while True:
#             if j >= len(tag):
#                 break
#             temp_indicate = tag[j][0]

#             if temp_indicate == "/object":
#                 xml_start = -1
#                 value_pos_temp = []
#                 object_pos_temp = []
                
#                 value_value = value_pos = ""
#                 object_value = object_pos = ""
#                 status_value = agreement_value = type_value = ""
#                 object_index_start = object_index_end = 0
#                 agreement_index = 0
#                 status_index = 0
#                 type_index = 0
#                 id_index = 0
#                 value_index_start = value_index_end = 0
#                 agreement_present = True
#                 type_present = status_present = False
#                 golden = False
                
                
#                 current_index = j
#                 while True:
#                     current_index -= 1
#                     if ( str(tag[current_index][0]) == "<" ):
#                         object_index_end = current_index-1
#                         break
#                 while True:
#                     current_index -= 1
#                     if ( str(tag[current_index][0]) == ">" and str(tag[current_index-5][0]) == "agreement" ):
#                         if str(tag[current_index-2][0]) == "ems":
#                             golden = True
#                         object_index_start = current_index+1
#                         agreement_index = current_index-2
#                         break
#                 while True:
#                     current_index -= 1
#                     if ( str(tag[current_index][0]) == "status" and not status_present ):
#                         status_present = True
#                         status_index = current_index+3
#                     if ( str(tag[current_index][0]) == "type" and not type_present ):
#                         type_present = True
#                         type_index = current_index+3
#                         break
#                     if current_index < object_index_start - 16:
#                         break
#                 while True:
#                     current_index -= 1
#                     if ( str(tag[current_index][0]) == "id" ):
#                         id_index = current_index+3
#                         value_index_end = current_index-2
#                         break
#                 while True:
#                     current_index -= 1
#                     if ( str(tag[current_index][0]) == "value" and str(tag[current_index-1][0]) == "object" and str(tag[current_index-2][0]) == "<" ):
#                         value_index_start = current_index+3
#                         xml_start = current_index - 2
#                         break
            

#                 while value_index_start <= value_index_end:
# #                    print "value_index: " , value_index_start
#                     if value_index_start < len(tag):
# #                        print "yes value"
#                         value_value = value_value + str(tag[value_index_start][0]) + " "
#                         value_pos = value_pos + str(tag[value_index_start][0]) + " "
#                     value_index_start += 1
                        
#                 while object_index_start <= object_index_end:
# #                    print "object_index: " , object_index_start
#                     if object_index_start < len(tag):
# #                        print "yes object"
#                         object_value = object_value + str(tag[object_index_start][0]) + " "
#                         object_pos = object_pos + str(tag[object_index_start][0]) + " "
#                     object_index_start += 1
                
#                 agreement_value = str(tag[agreement_index][0])
#                 if type_present:
#                     type_value = str(tag[type_index][0])
#                 if status_present:
#                     status_value = str(tag[status_index][0])
#                 id_value = str(tag[id_index][0])
#                 #            print "YESSSSS"
#                 line_no = i
#                 blog_id = filenum_list[round]
                
#                 object_value = object_value.replace(" \\", "")
#                 object_value = object_value.replace("\\", "")
#                 object_value = object_value.replace("\\ ", "")
#                 object_value = object_value.replace(" /'", "")

#                 get_index( tag, object_index_start )

#                 # notag_sentence_index = 0
#                 # notag_sentence = ""
#                 # for notag_sentence_index in range(0, xml_start):
#                 #     notag_sentence = notag_sentence + " " + str(tag[notag_sentence_index][0])
#                 # notag_sentence += object_value
#                 # notag_sentence_index = j + 2
#                 # print "j + 2 = " + str(notag_sentence_index)
#                 # while notag_sentence_index < len(tag):
#                 #     notag_sentence = notag_sentence + " " + str(tag[notag_sentence_index][0])
#                 #     notag_sentence_index += 1
#                 # print "notag sentence: "
#                 # print notag_sentence

#                 print "id_value: " + id_value
#                 print "value_value: " + value_value
#                 print "type_value: " + type_value
#                 print "status_value: " + status_value
#                 print "object_value: " + object_value
#                 print "agreement_value: " + agreement_value
#                 file5.write( "\nblod_id: " + str(blog_id) + "\n" )
#                 file5.write( "line_no: " + str(line_no) + "\n" )
#                 file5.write( "id: " + str(id_value) + "\n" )
#                 file5.write( "type: " + str(type_value) + "\n" )
#                 file5.write( "status: " + str(status_value) + "\n" )
#                 file5.write( "agreement: " + str(agreement_value) + "\n" )
#                 file5.write( "value: " + str(value_value) + "\n" )
#                 file5.write( "object: " + str(object_value) + "\n" )


#                 print "blog_id: ", blog_id, ", line_no: " , line_no, "object: ", object_value, ", object pos: ", object_pos, ", object identified as ", value_value, " which is " , value_pos

#             j += 1
#         i += 1















