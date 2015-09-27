
from xml.dom.minidom import Document, parseString
#from __future__ import print_function, division
from collections import Counter, defaultdict
    
import nltk, re, pprint
from nltk import word_tokenize
    
filenum_list = [1,2,3,4,5,6,7, 8, 9,10,11,12,13,14,15, 16, 17, 18,19,20,21,22,23,24, 25, 26, 27];


total_value_pos_dict = dict()
total_object_pos_dict = dict()

total_golden_value_pos_dict = dict()
total_golden_object_pos_dict = dict()


# file5 = open( "stat/total_stat.txt", "w")
file6 = open( "stat/total_object.txt", "w")
# file7 = open( "stat/total_clean_sentence.txt", "w")

for round in range(0, len(filenum_list)):
# for round in range(0, 1):
    filename = 'Blog ' + str(filenum_list[round]) + '_reconciled.xml'
    # filename = 'Blog 20_reconciled.xml'
    filename_alone = filename.rsplit('.', 1)[0]
    file = open("reconcile/" + filename, 'r')
    
    sentences = str(file.readlines())
    print "blog_id: ", filenum_list[round]
    # file7.write(str(filenum_list[round]) + "\n")
    #sentences = "Call me Ishmael. Some years ago - never mind how long precisely - having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world."
    
    tagged = nltk.sent_tokenize(sentences.strip())
    tagged = [nltk.word_tokenize(sent) for sent in tagged]
    tagged = [nltk.pos_tag(sent) for sent in tagged]
    
    # value_pos_dict = dict()
    # object_pos_dict = dict()
    
    # golden_target_object_value = []
    # golden_target_object_pos = []
    # golden_target_value_value = []
    # golden_target_value_pos = []

    # golden_object_pos_dict = dict()
    # golden_value_pos_dict = dict()
    
    i = 0
    noun_id = 0
    for tag in tagged:
        j = 0
        # print "i = " , i, ", tag = "
        # print tag
        # get original pos
        to_get_clean_pos_index = 0
        to_get_clean_sentence = ""
        raw_i = 0
        while to_get_clean_pos_index < len(tag):
            # print str(to_get_clean_pos_index) + ": " , tag[to_get_clean_pos_index][0]
            while to_get_clean_pos_index < len(tag) and tag[to_get_clean_pos_index][0] != "<" :
                # print str(to_get_clean_pos_index) + ": " , tag[to_get_clean_pos_index][0] , " != <"
                to_get_clean_sentence += " " + tag[to_get_clean_pos_index][0]
                to_get_clean_pos_index += 1
                raw_i += 1
            if to_get_clean_pos_index >= len(tag):
                break
            while to_get_clean_pos_index < len(tag) and ">" not in tag[to_get_clean_pos_index][0]:
                # print str(to_get_clean_pos_index) + ": " , tag[to_get_clean_pos_index][0] , " != e>"
                to_get_clean_pos_index += 1
            if to_get_clean_pos_index >= len(tag):
                break
            to_get_clean_pos_index += 1
            while to_get_clean_pos_index < len(tag) and "<" not in tag[to_get_clean_pos_index][0]:
                # if i == current_index:
                    # clean_index = raw_i
                # print "object: " , tag[to_get_clean_pos_index][0]
                to_get_clean_sentence += " " + tag[to_get_clean_pos_index][0]
                raw_i += 1
                to_get_clean_pos_index += 1
                # print str(to_get_clean_pos_index) + ": " , tag[to_get_clean_pos_index][0]
            # print "\n"
            if to_get_clean_pos_index >= len(tag):
                break
            to_get_clean_pos_index += 3

        # print "clean sentence: "
        # print to_get_clean_sentence

        to_get_clean_sentence = to_get_clean_sentence.lower()
        clean_text = word_tokenize(to_get_clean_sentence)
        clean_tag = nltk.pos_tag(clean_text)
        # file7.write(to_get_clean_sentence + "\n")

        # print "clean_tag: "
        # print clean_tag
        # print "\n\n"

        while True:
            if j >= len(tag):
                break            

            temp_indicate = tag[j][0]
            if temp_indicate == "/object":
                xml_start = -1
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
                agreement_present = False
                type_present = status_present = False
                golden = False
                
                current_index = j
                while True:
                    current_index -= 1
                    if ( str(tag[current_index][0]) == "<" ):
                        object_index_end = current_index-1
                        break
                while True:
                    current_index -= 1
                    if ( str(tag[current_index][0]) == ">" and str(tag[current_index-5][0]) == "agreement" ):
                        if len(str(tag[current_index-2][0])) == 3: # ems / sem
                            golden = True
                        object_index_start = current_index+1
                        agreement_index = current_index-2
                        break
                    if ( str(tag[current_index][0]) == ">" and str(tag[current_index-5][0]) != "agreement" ):
                        object_index_start = current_index+1
                        break
                while True:
                    current_index -= 1
                    if ( str(tag[current_index][0]) == "status" and not status_present ):
                        status_present = True
                        status_index = current_index+3
                    if ( str(tag[current_index][0]) == "type" and not type_present ):
                        type_present = True
                        type_index = current_index+3
                        break
                    if current_index < object_index_start - 16:
                        break
                while True:
                    current_index -= 1
                    if ( str(tag[current_index][0]) == "id" ):
                        id_index = current_index+3
                        value_index_end = current_index-2
                        break

                while True:
                    current_index -= 1
                    # print "current index: " , current_index, ": " , tag[current_index][0]
                    if ( str(tag[current_index][0]) == "value" and str(tag[current_index-1][0]) == "object" and str(tag[current_index-2][0]) == "<" ):
                        value_index_start = current_index+3
                        xml_start = current_index - 2
                        break
                # print "object_index_start: " , object_index_start, ": " , tag[object_index_start][0]
                # print "object_index_end: ", object_index_end, ": " , tag[object_index_end][0]
                # print "value_index_end: " , value_index_end
                # print "current index: " , current_index, ": " , tag[current_index][0]
                # print "id index: " , id_index, ": " , tag[id_index][0]
                # print "agreement index: ", agreement_index
                # print "type index: ", type_index
                # print "status index: ", status_index
#                features
#                 while value_index_start <= value_index_end:
# #                    print "value_index: " , value_index_start
#                     if value_index_start < len(tag):
# #                        print "yes value"
#                         value_value = value_value + str(tag[value_index_start][0]) + " "
#                         value_pos = value_pos + str(tag[value_index_start][0]) + " "
# #                        value_pos_temp.append( str(tag[value_index_start][0]) )
#                         if str(tag[value_index_start][1]) in total_value_pos_dict:
#                             total_value_pos_dict[str(tag[value_index_start][1])] += 1
#                         #                            file.write( str_object + ":     " + str_pos + " in dict, update count to " + str(pos_dict[str_pos]) + "\n" )
#                         else:
#                             total_value_pos_dict[str(tag[value_index_start][1])] = 1
# #                            file.write( str_object + ":     " + str_pos + " not in dict, set to " + str(pos_dict[str_pos]) + "\n" )
#                         if golden:
#                             if str(tag[value_index_start][1]) in total_golden_value_pos_dict:
#                                 total_golden_value_pos_dict[str(tag[value_index_start][1])] += 1
# #                        file.write( str_object + ":     " + str_pos + " in dict, update count to " + str(golden_pos_dict[str_pos]) + "\n" )
#                             else:
#                                 total_golden_value_pos_dict[str(tag[value_index_start][1])] = 1
# #                        file.write( str_object + ":     " + str_pos + " not in dict, set to " + str(golden_pos_dict[str_pos]) + "\n" )
#                             golden_target_value_value.append( str(tag[value_index_start][0]) )
#                             golden_target_value_pos.append( str(tag[value_index_start][1]) )
#                     value_index_start += 1
                            
                while object_index_start <= object_index_end:
                    # print "object_index: " , object_index_start
                    if object_index_start < len(tag):
                        # print "yes object: " , tag[object_index_start][0]
                        object_value = object_value + str(tag[object_index_start][0]) + " "
                        object_pos = object_pos + str(tag[object_index_start][0]) + " "
#                        object_pos_temp.append( str(tag[object_index_start][0]) )
                        if str(tag[object_index_start][1]) in total_object_pos_dict:
                            total_object_pos_dict[str(tag[object_index_start][1])] += 1
#                            file.write( str_object + ":     " + str_pos + " in dict, update count to " + str(pos_dict[str_pos]) + "\n" )
                        else:
                            total_object_pos_dict[str(tag[object_index_start][1])] = 1
#                            file.write( str_object + ":     " + str_pos + " not in dict, set to " + str(pos_dict[str_pos]) + "\n" )
                        if golden:
                            if str(tag[object_index_start][1]) in total_golden_object_pos_dict:
                                total_golden_object_pos_dict[str(tag[object_index_start][1])] += 1
#                        file.write( str_object + ":     " + str_pos + " in dict, update count to " + str(golden_pos_dict[str_pos]) + "\n" )
                            else:
                                total_golden_object_pos_dict[str(tag[object_index_start][1])] = 1
#                        file.write( str_object + ":     " + str_pos + " not in dict, set to " + str(golden_pos_dict[str_pos]) + "\n" )
                            # golden_target_object_value.append( str(tag[object_index_start][0]) )
                            # golden_target_object_pos.append( str(tag[object_index_start][1]) )
                    object_index_start += 1
               
                
                agreement_value = str(tag[agreement_index][0])
                if type_present:
                    type_value = str(tag[type_index][0])
                if status_present:
                    status_value = str(tag[status_index][0])
                id_value = str(tag[id_index][0])
                #            print "YESSSSS"
                line_no = i
                blog_id = filenum_list[round]
                
                object_value = object_value.replace(" \\", "")
                object_value = object_value.replace("\\", "")
                object_value = object_value.replace("\\ ", "")
                object_value = object_value.replace(" /'", "")
                # print "\nxml_start: " , xml_start
                # print "object_index_start: " , object_index_start
                # print "object_index_end: ", object_index_end
                # print "value_index_start:", value_index_start
                # print "value_index_end: " , value_index_end
                # print "object: " , object_value
                # print "blog_id: ", blog_id
                # print to_get_clean_sentence
                file6.write( str(object_value) + "\n" )
                # print "noun_to_check size: ", len(noun_to_check)
                # print "verb_to_check size: ", len(verb_to_check)
                # print "adj_to_check size: ", len(adj_to_check)
                # for noun in noun_to_check:
                #     if noun in object_value and noun in to_get_clean_sentence:
                #         if noun+"es" in dict(clean_tag):
                #             noun = noun+"es"
                #         elif noun+"s" in dict(clean_tag):
                #             noun = noun+"es"
                #         if noun in dict(clean_tag): #and (str(dict(clean_tag)[noun]).lower())[0] == "n":
                #             print "\n\n"
                #             print "blog_id: ", blog_id, ", line_no: " , line_no, ", noun_id: ", id_index, "object: ", object_value, ", object identified as ", value_value
                #             # print "clean sentence: "
                #             # print to_get_clean_sentence
                #             # print "clean_tag: "
                #             # print clean_tag
                #             print  "noun     ", noun , " in clean tag pos: " , dict(clean_tag)[noun]
                #             file5.write( "\nnoun " + str(noun) + " n clean tag pos: " +str(dict(clean_tag)[noun] )+"\n" )
                #             file5.write( "\nblod_id: " + str(blog_id) + "\n" )
                #             # file5.write( "line_no: " + str(line_no) + "\n" )
                #             # file5.write( "id: " + str(id_value) + "\n" )
                #             # file5.write( "type: " + str(type_value) + "\n" )
                #             # file5.write( "status: " + str(status_value) + "\n" )
                #             # file5.write( "agreement: " + str(agreement_value) + "\n" )
                #             # file5.write( "value: " + str(value_value) + "\n" )
                #             file5.write( "object: " + str(object_value) + "\n" )
                #             # file5.write( "noun in clean sentence: " + str(noun) + "\n" )
                #             file5.write( "noun in clean sentence pos: " + str(dict(clean_tag)[noun]) + "\n" )
                #             file5.write( "\nclean sentence: " + str(to_get_clean_sentence) + "\n" )
                #             file5.write( "\nclean tag: " + str(clean_tag) + "\n" )
                #             if noun in noun_to_check_dict:
                #                 noun_to_check_dict[noun] += 1
                #             else:
                #                 noun_to_check_dict[noun] = 1
                #             if (str(dict(clean_tag)[noun]).lower())[0] == "n":
                #                 if noun in strict_noun_to_check_dict:
                #                     strict_noun_to_check_dict[noun] += 1
                #                 else:
                #                     strict_noun_to_check_dict[noun] = 1
                # for verb in verb_to_check:
                #     if verb in object_value and verb in to_get_clean_sentence:
                #         if verb+"ed" in dict(clean_tag):
                #             verb = verb+"ed"
                #         elif verb+"d" in dict(clean_tag):
                #             verb = verb+"d"
                #         if verb in dict(clean_tag): #and (str(dict(clean_tag)[verb]).lower())[0] == "v":
                #             print "\n\n"
                #             print "blog_id: ", blog_id, ", line_no: " , line_no, ", noun_id: ", id_index, "object: ", object_value, ", object identified as ", value_value
                #             # print "clean sentence: "
                #             # print to_get_clean_sentence
                #             # print "clean_tag: "
                #             # print clean_tag
                #             print  "verb     ", verb , " in clean tag pos: " , dict(clean_tag)[verb]
                #             file5.write( "\nverb " + str(verb) + " n clean tag pos: " + str(dict(clean_tag)[verb])+ "\n" )
                #             file5.write( "\nblod_id: " + str(blog_id) + "\n" )
                #             # file5.write( "line_no: " + str(line_no) + "\n" )
                #             # file5.write( "id: " + str(id_value) + "\n" )
                #             # file5.write( "type: " + str(type_value) + "\n" )
                #             # file5.write( "status: " + str(status_value) + "\n" )
                #             # file5.write( "agreement: " + str(agreement_value) + "\n" )
                #             # file5.write( "value: " + str(value_value) + "\n" )
                #             file5.write( "object: " + str(object_value) + "\n" )
                #             # file5.write( "verb in clean sentence: " + str(noun) + "\n" )
                #             file5.write( "verb in clean sentence pos: " + str(dict(clean_tag)[verb]) + "\n" )
                #             file5.write( "\nclean sentence: " + str(to_get_clean_sentence) + "\n" )
                #             file5.write( "\nclean tag: " + str(clean_tag) + "\n" )
                #             if verb in verb_to_check_dict:
                #                 verb_to_check_dict[verb] += 1
                #             else:
                #                 verb_to_check_dict[verb] = 1
                #             if (str(dict(clean_tag)[verb]).lower())[0] == "v":
                #                 if verb in strict_verb_to_check_dict:
                #                     strict_verb_to_check_dict[verb] += 1
                #                 else:
                #                     strict_verb_to_check_dict[verb] = 1
                # for adj in adj_to_check:
                #     if adj in object_value and adj in to_get_clean_sentence:
                #         if adj in dict(clean_tag): #and (str(dict(clean_tag)[noun]).lower())[0] == "j":
                #             print "\n\n"
                #             print "blog_id: ", blog_id, ", line_no: " , line_no, ", noun_id: ", id_index, "object: ", object_value,  ", object identified as ", value_value
                #             # print "clean sentence: "
                #             # print to_get_clean_sentence
                #             # print "clean_tag: "
                #             # print clean_tag
                #             print  "adj     ", adj , " in clean tag pos: " , dict(clean_tag)[adj]
                #             file5.write( "\nadj " + str(adj) + " n clean tag pos: " +str(dict(clean_tag)[adj])+"\n" )
                #             file5.write( "\nblod_id: " + str(blog_id) + "\n" )
                #             # file5.write( "line_no: " + str(line_no) + "\n" )
                #             # file5.write( "id: " + str(id_value) + "\n" )
                #             # file5.write( "type: " + str(type_value) + "\n" )
                #             # file5.write( "status: " + str(status_value) + "\n" )
                #             # file5.write( "agreement: " + str(agreement_value) + "\n" )
                #             # file5.write( "value: " + str(value_value) + "\n" )
                #             file5.write( "object: " + str(object_value) + "\n" )
                #             # file5.write( "adj in clean sentence: " + str(noun) + "\n" )
                #             file5.write( "adj in clean sentence pos: " + str(dict(clean_tag)[adj]) + "\n" )
                #             file5.write( "\nclean sentence: " + str(to_get_clean_sentence) + "\n" )
                #             file5.write( "\nclean tag: " + str(clean_tag) + "\n" )
                #             if adj in adj_to_check_dict:
                #                 adj_to_check_dict[adj] += 1
                #             else:
                #                 adj_to_check_dict[adj] = 1
                #             if (str(dict(clean_tag)[adj]).lower())[0] == "j":
                #                 if adj in strict_adj_to_check_dict:
                #                     strict_adj_to_check_dict[adj] += 1
                #                 else:
                #                     strict_adj_to_check_dict[adj] = 1

                
                noun_id += 1
            j += 1
        i += 1
    tagged = str(tagged)
    file.close()

# for key, value in noun_to_check_dict.iteritems():
#     print key, ' has count ', noun_to_check_dict[key]
#     file5.write( str(key) + " has count " + str(noun_to_check_dict[key]) + "\n" )


# for key, value in verb_to_check_dict.iteritems():
#     print key, ' has count ', verb_to_check_dict[key]
#     file5.write( str(key) + " has count " + str(verb_to_check_dict[key]) + "\n" )


# for key, value in adj_to_check_dict.iteritems():
#     print key, ' has count ', adj_to_check_dict[key]
#     file5.write( str(key) + " has count " + str(adj_to_check_dict[key]) + "\n" )

# for key, value in strict_noun_to_check_dict.iteritems():
#     print key, ' has strict_count ', strict_noun_to_check_dict[key]
#     file5.write( str(key) + " has strict_count " + str(strict_noun_to_check_dict[key]) + "\n" )


# for key, value in strict_verb_to_check_dict.iteritems():
#     print key, ' has strict_count ', strict_verb_to_check_dict[key]
#     file5.write( str(key) + " has strict_count " + str(strict_verb_to_check_dict[key]) + "\n" )


# for key, value in strict_adj_to_check_dict.iteritems():
#     print key, ' has strict_count ', strict_adj_to_check_dict[key]
#     file5.write( str(key) + " has strict_count " + str(strict_adj_to_check_dict[key]) + "\n" )



# file5.close()
file6.close()
# file7.close()



































