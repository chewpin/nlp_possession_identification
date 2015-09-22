
from xml.dom.minidom import Document, parseString
#from __future__ import print_function, division
from collections import Counter
    
import nltk, re, pprint
from nltk import word_tokenize
    
filenum_list = [7, 8, 9, 16, 17, 18, 25, 26, 27];

indicator_feature_2d = []
indicator_feature_2d.append([]) # 0 indicator_name
indicator_feature_2d.append([]) # 1 count of met
indicator_feature_2d.append([]) # 2 count of actual (use)

indicator_feature_2d[0].append("general_pronoun")
indicator_feature_2d[0].append("general_adj_pronoun")
indicator_feature_2d[0].append("general_appearance_descriptor")
indicator_feature_2d[0].append("general_verb")
indicator_feature_2d[0].append("general_noun")
indicator_feature_2d[0].append("brand_noun")
indicator_feature_2d[0].append("component_noun")

general_pronoun_dict_met = dict()
general_pronoun_dict_actual = dict()
general_adj_dict_met = dict()
general_adj_dict_actual = dict()

for i in range(0,10):
    indicator_feature_2d[1].append(0)
for i in range(0,10):
    indicator_feature_2d[2].append(0)


total_value_pos_dict = dict()
total_object_pos_dict = dict()

total_golden_value_pos_dict = dict()
total_golden_object_pos_dict = dict()
file5 = open( "total_pos.txt", "w")

def is_general_pronoun(temp_indicate):
    return temp_indicate in ["my", "our", "this", "that", "those", "these"]
def is_general_adj(temp_indicate):
    return temp_indicate in ["favorite", "new", "old", "some", "other", "best", "same", "good", "own", "modern", "entire"]

for round in range(0, len(filenum_list)):
    filename = 'Blog' + str(filenum_list[round]) + '_eadsit_reconciled.xml'
#    filename = 'Blog27_eadsit_reconciled.xml'
    filename_alone = filename.rsplit('.', 1)[0]
    file = open(filename, 'r')
    
    sentences = str(file.readlines())
    #sentences = "Call me Ishmael. Some years ago - never mind how long precisely - having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world."
    
    tagged = nltk.sent_tokenize(sentences.strip())
    tagged = [nltk.word_tokenize(sent) for sent in tagged]
    tagged = [nltk.pos_tag(sent) for sent in tagged]
    
    #counts = Counter(tag for word,tag in tagged)
    #print counts
    file = open( filename_alone + "_pos.txt", "w")
    file2 = open( filename_alone + "_pos_complete.txt", "w")
    file3 = open( filename_alone + "_pos_detail.txt", "w")
    
#    target_object = []
#    target_pos = []

    value_pos_dict = dict()
    object_pos_dict = dict()
    
    golden_target_object_value = []
    golden_target_object_pos = []
    golden_target_value_value = []
    golden_target_value_pos = []

    golden_object_pos_dict = dict()
    golden_value_pos_dict = dict()
    
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
            if is_general_pronoun(temp_indicate):
                indicator_feature_2d[1][0] += 1
                if str(temp_indicate) in general_pronoun_dict_met:
                    general_pronoun_dict_met[str(temp_indicate)] += 1
                else:
                    general_pronoun_dict_met[str(temp_indicate)] = 1
                        
            if is_general_adj(temp_indicate):
                indicator_feature_2d[1][1] += 1
                if str(temp_indicate) in general_adj_dict_met:
                    general_adj_dict_met[str(temp_indicate)] += 1
                else:
                    general_adj_dict_met[str(temp_indicate)] = 1
            
            #        print "[[[" + temp_indicate + "]]]"
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
                agreement_present = True
                type_present = status_present = False
                golden = False
                
                general_pronoun_indicator_temp = general_adj_indicator_temp = -1
                
                current_index = j
                while True:
                    current_index -= 1
                    if ( str(tag[current_index][0]) == "<" ):
                        object_index_end = current_index-1
                        break
                while True:
                    current_index -= 1
                    if ( str(tag[current_index][0]) == ">" and str(tag[current_index-5][0]) == "agreement" ):
                        if str(tag[current_index-2][0]) == "ems":
                            golden = True
                        object_index_start = current_index+1
                        agreement_index = current_index-2
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
                    if ( str(tag[current_index][0]) == "value" and str(tag[current_index-1][0]) == "object" and str(tag[current_index-2][0]) == "<" ):
                        value_index_start = current_index+3
                        xml_start = current_index - 2
                        break
#                features
                if ( xml_start != -1 ):
                    if is_general_pronoun(str(tag[xml_start-1][0])):
                        indicator_feature_2d[2][0] += 1
                        general_pronoun_indicator_temp = str(tag[xml_start-1][0])
                        if str(tag[xml_start-1][0]) in general_pronoun_dict_actual:
                            general_pronoun_dict_actual[str(tag[xml_start-1][0])] += 1
                        else:
                            general_pronoun_dict_actual[str(tag[xml_start-1][0])] = 1

                if ( xml_start != -1 ):
                    if is_general_adj(str(tag[xml_start-1][0])):
                        indicator_feature_2d[2][1] += 1
                        general_adj_indicator_temp = str(tag[xml_start-1][0])
                        if str(tag[xml_start-1][0]) in general_adj_dict_actual:
                            general_adj_dict_actual[str(tag[xml_start-1][0])] += 1
                        else:
                            general_adj_dict_actual[str(tag[xml_start-1][0])] = 1
            

                while value_index_start <= value_index_end:
#                    print "value_index: " , value_index_start
                    if value_index_start < len(tag):
#                        print "yes value"
                        value_value = value_value + str(tag[value_index_start][0]) + " "
                        value_pos = value_pos + str(tag[value_index_start][0]) + " "
#                        value_pos_temp.append( str(tag[value_index_start][0]) )
                        if str(tag[value_index_start][1]) in value_pos_dict:
                            value_pos_dict[str(tag[value_index_start][1])] += 1
                        #                            file.write( str_object + ":     " + str_pos + " in dict, update count to " + str(pos_dict[str_pos]) + "\n" )
                        else:
                            value_pos_dict[str(tag[value_index_start][1])] = 1
#                            file.write( str_object + ":     " + str_pos + " not in dict, set to " + str(pos_dict[str_pos]) + "\n" )
                        if golden:
                            if str(tag[value_index_start][1]) in golden_value_pos_dict:
                                golden_value_pos_dict[str(tag[value_index_start][1])] += 1
#                        file.write( str_object + ":     " + str_pos + " in dict, update count to " + str(golden_pos_dict[str_pos]) + "\n" )
                            else:
                                golden_value_pos_dict[str(tag[value_index_start][1])] = 1
#                        file.write( str_object + ":     " + str_pos + " not in dict, set to " + str(golden_pos_dict[str_pos]) + "\n" )
                            golden_target_value_value.append( str(tag[value_index_start][0]) )
                            golden_target_value_pos.append( str(tag[value_index_start][1]) )
                    value_index_start += 1
                        
                while object_index_start <= object_index_end:
#                    print "object_index: " , object_index_start
                    if object_index_start < len(tag):
#                        print "yes object"
                        object_value = object_value + str(tag[object_index_start][0]) + " "
                        object_pos = object_pos + str(tag[object_index_start][0]) + " "
#                        object_pos_temp.append( str(tag[object_index_start][0]) )
                        if str(tag[object_index_start][1]) in object_pos_dict:
                            object_pos_dict[str(tag[object_index_start][1])] += 1
#                            file.write( str_object + ":     " + str_pos + " in dict, update count to " + str(pos_dict[str_pos]) + "\n" )
                        else:
                            object_pos_dict[str(tag[object_index_start][1])] = 1
#                            file.write( str_object + ":     " + str_pos + " not in dict, set to " + str(pos_dict[str_pos]) + "\n" )
                        if golden:
                            if str(tag[object_index_start][1]) in golden_object_pos_dict:
                                golden_object_pos_dict[str(tag[object_index_start][1])] += 1
#                        file.write( str_object + ":     " + str_pos + " in dict, update count to " + str(golden_pos_dict[str_pos]) + "\n" )
                            else:
                                golden_object_pos_dict[str(tag[object_index_start][1])] = 1
#                        file.write( str_object + ":     " + str_pos + " not in dict, set to " + str(golden_pos_dict[str_pos]) + "\n" )
                            golden_target_object_value.append( str(tag[object_index_start][0]) )
                            golden_target_object_pos.append( str(tag[object_index_start][1]) )
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
                print "id_value: " + id_value
                print "value_value: " + value_value
                print "type_value: " + type_value
                print "status_value: " + status_value
                print "object_value: " + object_value
                print "agreement_value: " + agreement_value
                file3.write( "\nblod_id: " + str(blog_id) + "\n" )
                file3.write( "line_no: " + str(line_no) + "\n" )
                file3.write( "id: " + str(id_value) + "\n" )
                file3.write( "type: " + str(type_value) + "\n" )
                file3.write( "status: " + str(status_value) + "\n" )
                file3.write( "agreement: " + str(agreement_value) + "\n" )
                file3.write( "value: " + str(value_value) + "\n" )
                file3.write( "object: " + str(object_value) + "\n" )
                if general_pronoun_indicator_temp != -1:
                    file3.write( "general_pronoun_indicator: " + general_pronoun_indicator_temp + "\n" )
                if general_adj_indicator_temp != -1:
                    file3.write( "general_adj_indicator_temp: " + general_adj_indicator_temp + "\n" )

                print "blog_id: ", blog_id, ", line_no: " , line_no, ", nound_id: ", noun_id, "object: ", object_value, ", object pos: ", object_pos, ", object identified as ", value_value, " which is " , value_pos

#                target_object.append( str(object_value) )
#                target_pos.append( str(object_pos) )
#                if j > 5 and str(tag[j-5][0]) == "ems":
#                    print "golden"
#                    if str_pos in golden_pos_dict:
#                        golden_pos_dict[str_pos] += 1
##                        file.write( str_object + ":     " + str_pos + " in dict, update count to " + str(golden_pos_dict[str_pos]) + "\n" )
#                    else:
#                        golden_pos_dict[str_pos] = 1
##                        file.write( str_object + ":     " + str_pos + " not in dict, set to " + str(golden_pos_dict[str_pos]) + "\n" )
#                    golden_target_object.append( str_object )
#                    golden_target_pos.append( str_pos )
                noun_id += 1
            j += 1
        i += 1
#    for x in range(0, len(target_object)):
#        print target_object[x]
#        print target_pos[x]
    print "value:"
    for key, value in value_pos_dict.iteritems():
        print key, 'corresponds to', value_pos_dict[key]
        file.write( "\n" + str(key) + " has count " + str(value_pos_dict[key]) + "\n" )
    print "object:"
    for key, value in object_pos_dict.iteritems():
        print key, 'corresponds to', object_pos_dict[key]
        file.write( "\n" + str(key) + " has count " + str(object_pos_dict[key]) + "\n" )
    tagged = str(tagged)
    file.write("\n\n\n\n\n\n\n\n\n\n")
    file.write(tagged)
    file.close()
    file4 = open( filename_alone + "_pos_only.txt", "w")

    file4.write("\nTotal object statistics:\n")
    print "Total:"
    for key, value in object_pos_dict.iteritems():
        if key in total_object_pos_dict:
            total_object_pos_dict[key] += object_pos_dict[key]
        else:
            total_object_pos_dict[key] = 1
        print key, 'corresponds to', object_pos_dict[key]
        file4.write( str(key) + " has count " + str(object_pos_dict[key]) + "\n" )
    file4.write("\nTotal value statistics:\n")
    print "Total:"
    for key, value in value_pos_dict.iteritems():
        if key in total_value_pos_dict:
            total_value_pos_dict[key] += value_pos_dict[key]
        else:
            total_value_pos_dict[key] = 1
        print key, 'corresponds to', value_pos_dict[key]
        file4.write( str(key) + " has count " + str(value_pos_dict[key]) + "\n" )

    file4.write("\nGolden Standard object statistics:\n")
    print "Golden object:"
    for key, value in golden_object_pos_dict.iteritems():
        if key in total_golden_object_pos_dict:
            total_golden_object_pos_dict[key] += golden_object_pos_dict[key]
        else:
            total_golden_object_pos_dict[key] = 1
        print key, 'corresponds to', golden_object_pos_dict[key]
        file4.write( str(key) + " has count " + str(golden_object_pos_dict[key]) + "\n" )
    file4.write("\nGolden Standard value statistics:\n")
    print "Golden object:"
    for key, value in golden_value_pos_dict.iteritems():
        if key in total_golden_value_pos_dict:
            total_golden_value_pos_dict[key] += golden_value_pos_dict[key]
        else:
            total_golden_value_pos_dict[key] = 1
        print key, 'corresponds to', golden_value_pos_dict[key]
        file4.write( str(key) + " has count " + str(golden_value_pos_dict[key]) + "\n" )
    file3.close()
    file2.close()
    file4.close()



print "Total object:"
file5.write("\nTotal object statistics:\n")
for key, value in total_object_pos_dict.iteritems():
    print key, 'corresponds to', total_object_pos_dict[key]
    file5.write( str(key) + " has count " + str(total_object_pos_dict[key]) + "\n" )


print "Total value:"
file5.write("\nTotal value statistics:\n")
for key, value in total_value_pos_dict.iteritems():
    print key, 'corresponds to', total_value_pos_dict[key]
    file5.write( str(key) + " has count " + str(total_value_pos_dict[key]) + "\n" )


print "Total golden object:"
file5.write("\nTotal golden Standard object statistics:\n")
for key, value in total_golden_object_pos_dict.iteritems():
    print key, 'corresponds to', total_golden_object_pos_dict[key]
    file5.write( str(key) + " has count " + str(total_golden_object_pos_dict[key]) + "\n" )


print "Total golden value:"
file5.write("\nTotal golden Standard value statistics:\n")
for key, value in total_golden_value_pos_dict.iteritems():
    print key, 'corresponds to', total_golden_value_pos_dict[key]
    file5.write( str(key) + " has count " + str(total_golden_value_pos_dict[key]) + "\n" )


# Loop over rows.
for row in indicator_feature_2d:
    # Loop over columns.
    for column in row:
        print column , " "
    print "\n"
print "general pronoun indicator:"
for key, value in general_pronoun_dict_met.iteritems():
    print key, ' has met count ', general_pronoun_dict_met[key]
print "\n"
for key, value in general_pronoun_dict_actual.iteritems():
    print key, ' has actual count ', general_pronoun_dict_actual[key]
print "\n\n\ngeneral adj indicator:"
for key, value in general_adj_dict_met.iteritems():
    print key, ' has met count ', general_adj_dict_met[key]
print "\n"
for key, value in general_adj_dict_actual.iteritems():
    print key, ' has actual count ', general_adj_dict_actual[key]













file5.close()




































