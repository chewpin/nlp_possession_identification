
from xml.dom.minidom import Document, parseString
#from __future__ import print_function, division
from collections import Counter, defaultdict
    
import nltk, re, pprint
from nltk import word_tokenize
import string
    

def check_word_valid (word, clean_tag):
    # print clean_tag
    word = str(word)
    if word == "<" or word == ">":
        return False
    if word.lower() not in dict(clean_tag):
        return False
    if str(dict(clean_tag)[word.lower()])[0].isalpha() or str(dict(clean_tag)[word.lower()]) =="-NONE-":
        return dict(clean_tag)[word.lower()]
    return False


invalidChars = set(string.punctuation.replace("_", ""))

picturable_word_list = ["angle", "ant", "apple", "arch", "arm", "army", "baby", "bag", "ball", "band", "basin", "basket", "bath", "bed", "bee", "bell", "berry", "bird", "blade", "board", "boat", "bone", "book", "boot", "bottle", "box", "boy", "brain", "brake", "branch", "brick", "bridge", "brush", "bucket", "bulb", "button", "cake", "camera", "card", "cart", "carriage", "cat", "chain", "cheese", "chest", "chin", "church", "circle", "clock", "cloud", "coat", "collar", "comb", "cord", "cow", "cup", "curtain", "cushion", "dog", "door", "drain", "drawer", "dress", "drop", "ear", "egg", "engine", "eye", "face", "farm", "feather", "finger", "fish", "flag", "floor", "fly", "foot", "fork", "fowl", "frame", "garden", "girl", "glove", "goat", "gun", "hair", "hammer", "hand", "hat", "head", "heart", "hook", "horn", "horse", "hospital", "house", "island", "jewel", "kettle", "key", "knee", "knife", "knot", "leaf", "leg", "library", "line", "lip", "lock", "map", "match", "monkey", "moon", "mouth", "muscle", "nail", "neck", "needle", "nerve", "net", "nose", "nut", "office", "orange", "oven", "parcel", "pen", "pencil", "picture", "pig", "pin", "pipe", "plane", "plate", "plow", "pocket", "pot", "potato", "prison", "pump", "rail", "rat", "receipt", "ring", "rod", "roof", "root", "sail", "school", "scissors", "screw", "seed", "sheep", "shelf", "ship", "shirt", "shoe", "skin", "skirt", "snake", "sock", "spade", "sponge", "spoon", "spring", "square", "stamp", "star", "station", "stem", "stick", "stocking", "stomach", "store", "street", "sun", "table", "tail", "thread", "throat", "thumb", "ticket", "toe", "tongue", "tooth", "town", "train", "tray", "tree", "trousers", "umbrella", "wall", "watch", "wheel", "whip", "whistle", "window", "wing", "wire", "worm"]

filenum_list = [1,2,3,4,5,6,7, 8, 9,10,11,12,13,14,15, 16, 17, 18,19,20,21,22,23,24, 25, 26, 27];
before_pos_dict = {}
after_pos_dict = {}
picturable_count_dict = {}
picture_dict = {}

file_error = open( "feature/error.txt", "w")
file_feature = open( "feature/feature.txt", "w" )
file_feature_original = open( "feature/feature_original.txt", "w" )
file_debug_pos = open("feature/debug_pos.txt", "w")


for round in range(0, len(filenum_list)):
# for round in range(0, 1):
    # file_feature.write( "\n\n" )
    filename = 'Blog ' + str(filenum_list[round]) + '_reconciled.xml'
    # filename = 'Blog 1_reconciled.xml'
    filename_alone = filename.rsplit('.', 1)[0]
    file = open("reconcile/" + filename, 'r')
    
    sentences = str(file.readlines())
    print "blog_id: ", filenum_list[round] ,"\n"
    # file7.write(str(filenum_list[round]) + "\n")
    #sentences = "Call me Ishmael. Some years ago - never mind how long precisely - having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world."
    
    tagged = nltk.sent_tokenize(sentences.strip())
    tagged = [nltk.word_tokenize(sent) for sent in tagged]
    tagged = [nltk.pos_tag(sent) for sent in tagged]
    i = 0
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

        # print "\n\n\n\n\n\n\n"
        # print "clean_tag: "
        # print clean_tag
        while True:
            if j >= len(tag):
                break    
            temp_indicate = tag[j][0]
            # print temp_indicate
            # if temp_indicate in dict(clean_tag):
                # if ( str(dict(clean_tag)[temp_indicate])[0].isalpha() or str(dict(clean_tag)[temp_indicate]) =="-NONE-" ):
            if temp_indicate == "/object":
                xml_start = -1                
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
                        agreement_present = True
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
                if agreement_present and len(str(tag[agreement_index][0])):
                    golden = True
                # print "object_index_start: " , object_index_start, ": " , tag[object_index_start][0]
                # print "object_index_end: ", object_index_end, ": " , tag[object_index_end][0]
                # print "value_index_end: " , value_index_end
                # print "current index: " , current_index, ": " , tag[current_index][0]
                # print "id index: " , id_index, ": " , tag[id_index][0]
                object_value_count = 0
                object_value_arr = []
                object_value_decode = ""  
                # first_time_temp = True  
                picturable = []  
                picturable_temp = []
                while object_index_start <= object_index_end:
                    # print "object_index: " , object_index_start
                    if object_index_start < len(tag):
                        object_value_arr.append(str(tag[object_index_start][0]))
                        temp = str(tag[object_index_start][0]).lower()
                        temp_decode = temp.replace("\\xe2\\x80\\xb2", "'") # erase some weird characters
                        temp_decode = temp_decode.replace("\\xe2\\x80\\x99", "'")
                        temp_decode = temp_decode.replace("\\xe2\\x80\\xa6", "...")
                        temp_decode = temp_decode.replace("\\xe2\\x80\\x9c", '"')
                        temp_decode = temp_decode.replace('\\', '')
                        if temp_decode.strip() in picturable_word_list:
                            picturable_temp.append( temp_decode.strip() )
                            picturable.append( picturable_word_list.index(temp_decode.strip()))
                            print temp_decode.strip() , " picturable: ", picturable_word_list.index(temp_decode.strip())
                        object_value_decode = object_value_decode + temp_decode + " "
                        object_value = object_value + str(tag[object_index_start][0]) + " "
                        object_pos = object_pos + str(tag[object_index_start][0]) + " " 
                        object_value_count += 1                      
                    object_index_start += 1

                id_value = str(tag[id_index][0])
                line_no = i
                blog_id = filenum_list[round] 
                insert = object_value.replace("\\xe2\\x80\\x99", "'")
                insert = insert.replace("\\xe2\\x80\\xb2", "'")
                insert = insert.replace("\\xe2\\x80\\xa6", "...")
                insert = insert.replace("\\xe2\\x80\\x9c", '"')
                insert = insert.replace('\\', '')
                if all(char in invalidChars for char in insert):
                    file_error.write( "\n[" + insert + "] is Invalid")
                file_feature.write( str(blog_id) + "_" + str(line_no) + "_" + str(id_value) + ", " + insert)
                file_feature_original.write( str(blog_id) + "_" + str(line_no) + "_" + str(id_value) + ", " + insert)
                current_index = xml_start-1
                feature_location_count = 1
                file_debug_pos.write("\n\n\n\n")
                # print "\n\nOBJECT: [" + str(object_value) + "]"
                while current_index >= 0 and current_index < len(tag) and feature_location_count < 6:
                    if tag[current_index][0] == "/object" :
                        current_index -= 2
                    elif tag[current_index][0] == ">" :
                        while tag[current_index][0] != "<" and current_index >= 0:
                            current_index -= 1
                    # print tag[current_index][0] 
                    file_debug_pos.write( str(tag[current_index][0]) + ": " + str(tag[current_index][1]) + "\n" )
                    if not check_word_valid(tag[current_index][0], clean_tag):
                        file_error.write( str(tag[current_index][0])+ " not valid")
                    elif '\\r' in str(tag[current_index][0]) or '"\\n"' in str(tag[current_index][0]):
                        # print "\n" + tag[current_index][0] , " contains '\\r' or '\\n' "
                        break
                    else:
                        # print " [", tag[current_index][0], "]: ", check_word_valid(tag[current_index][0], clean_tag), 
                        insert = str(tag[current_index][0]).replace("\\xe2\\x80\\x99", "'")
                        insert = insert.replace("\\xe2\\x80\\xb2", "'")
                        insert = insert.replace("\\xe2\\x80\\xa6", "...")
                        insert = insert.replace("\\xe2\\x80\\x9c", '"')
                        insert = insert.replace('\\', '')
                        if not all(char in invalidChars for char in insert):
                            feature_location_count += 1
                            if check_word_valid(tag[current_index][0], clean_tag) in before_pos_dict:
                                before_pos_dict[check_word_valid(tag[current_index][0], clean_tag)] += 1
                            else:
                                before_pos_dict[check_word_valid(tag[current_index][0], clean_tag)] = 1
                            file_feature.write( ", " + check_word_valid(tag[current_index][0], clean_tag) )
                            file_feature_original.write( ", " + insert )
                    current_index -= 1
                while ( feature_location_count < 6 ):
                    file_feature.write( ', ""' )
                    file_feature_original.write( ', ""' )
                    feature_location_count += 1
                file_debug_pos.write("\n\n")
                feature_location_count = 1
                current_index = j + 2
                while current_index >= 0 and current_index < len(tag) and feature_location_count < 6:
                    if tag[current_index][0] == "<" :
                        while tag[current_index][0] != ">" and current_index < len(tag):
                            current_index += 1
                    elif tag[current_index][0] == "/object" :
                        current_index += 2
                    # print tag[current_index][0] 
                    file_debug_pos.write( str(tag[current_index][0]) + ": " + str(tag[current_index][1]) + "\n" )
                    if not check_word_valid(tag[current_index][0], clean_tag):
                        file_error.write( str(tag[current_index][0])+ " not valid\n")
                    elif '\\r' in str(tag[current_index][0]) or '\\n' in str(tag[current_index][0]): 
                        # print "\n" + tag[current_index][0] , " contains '\\r' or '\\n' "                       
                        break
                    else:
                        # print " [", tag[current_index][0], "]: ", check_word_valid(tag[current_index][0], clean_tag), 
                        insert = str(tag[current_index][0]).replace("\\xe2\\x80\\x99", "'")
                        insert = insert.replace("\\xe2\\x80\\xb2", "'")
                        insert = insert.replace("\\xe2\\x80\\xa6", "...")
                        insert = insert.replace("\\xe2\\x80\\x9c", '"')
                        insert = insert.replace('\\', '')
                        if not all(char in invalidChars for char in insert):
                            feature_location_count += 1
                            if check_word_valid(tag[current_index][0], clean_tag) in after_pos_dict:
                                after_pos_dict[check_word_valid(tag[current_index][0], clean_tag)] += 1
                            else:
                                after_pos_dict[check_word_valid(tag[current_index][0], clean_tag)] = 1
                            file_feature.write( ", " + check_word_valid(tag[current_index][0], clean_tag) )
                            file_feature_original.write( ", " + insert )
                    current_index += 1
                while ( feature_location_count < 6 ):
                    file_feature.write( ', ""' )
                    file_feature_original.write( ', ""' )
                    feature_location_count += 1
                for index in picturable:
                    if index in picture_dict:
                        picture_dict[index] += 1
                    else:
                        picture_dict[index] = 1
                    file_feature.write( ", " + str(index) )
                    file_feature_original.write( ", " + str(picturable_word_list[index]) )
                file_feature.write( '\n' )
                file_feature_original.write( '\n' )
                # print "\n"

                object_value = object_value.replace(" \\", "")
                object_value = object_value.replace("\\", "")
                object_value = object_value.replace("\\ ", "")
                object_value = object_value.replace(" /'", "")
                object_value = object_value.strip()
               
                # print "\nxml_start: " , xml_start
                # print "object_index_start: " , object_index_start
                # print "object_index_end: ", object_index_end
                # print "value_index_start:", value_index_start
                # print "value_index_end: " , value_index_end
                # print "object: " , object_value
                # print "blog_id: ", blog_id
                # print to_get_clean_sentence
                # file6.write( "\n" + object_value_decode + "\n" )
                # file6.write( str(object_value) + "\n" )
                # print str(object_value)
                # print object_value
                            
            j += 1
        i += 1

    file.close()

file_feature.write("\n Stats for 5 words before POS:\n")
count = 0
for key, value in before_pos_dict.iteritems():
    count += before_pos_dict[key]
for key, value in before_pos_dict.iteritems():
    file_feature.write( str(key) + " has count " + str(before_pos_dict[key]) + "  ( " + 
        str("{0:.2f}".format(before_pos_dict[key] * 100 / float(count)) ) + "%)\n" )

file_feature.write("\n Stats for 5 words after POS:\n")
count = 0
for key, value in after_pos_dict.iteritems():
    count += after_pos_dict[key]
for key, value in after_pos_dict.iteritems():
    file_feature.write( str(key) + " has count " + str(after_pos_dict[key]) + "  ( " + 
        str("{0:.2f}".format(after_pos_dict[key] * 100 / float(count)) )+ "%)\n" )

file_feature.write("\n Stats for picturable words frequency:\n")
count = 0
for key, value in picture_dict.iteritems():
    count += picture_dict[key]
for key, value in picture_dict.iteritems():
    file_feature.write( str(key) + ": " + picturable_word_list[key] + " has count " + str(picture_dict[key]) + "  ( " + 
        str("{0:.2f}".format(picture_dict[key] * 100 / float(count)) )+ "%)\n" )
    


file_feature.close()
file_feature_original.close()
file_error.close()
file_debug_pos.close()































