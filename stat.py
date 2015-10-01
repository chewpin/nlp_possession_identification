
from xml.dom.minidom import Document, parseString
#from __future__ import print_function, division
from collections import Counter, defaultdict
    
import nltk, re, pprint
from nltk import word_tokenize
    
picturable_word_list = ["angle", "ant", "apple", "arch", "arm", "army", "baby", "bag", "ball", "band", "basin", "basket", "bath", "bed", "bee", "bell", "berry", "bird", "blade", "board", "boat", "bone", "book", "boot", "bottle", "box", "boy", "brain", "brake", "branch", "brick", "bridge", "brush", "bucket", "bulb", "button", "cake", "camera", "card", "cart", "carriage", "cat", "chain", "cheese", "chest", "chin", "church", "circle", "clock", "cloud", "coat", "collar", "comb", "cord", "cow", "cup", "curtain", "cushion", "dog", "door", "drain", "drawer", "dress", "drop", "ear", "egg", "engine", "eye", "face", "farm", "feather", "finger", "fish", "flag", "floor", "fly", "foot", "fork", "fowl", "frame", "garden", "girl", "glove", "goat", "gun", "hair", "hammer", "hand", "hat", "head", "heart", "hook", "horn", "horse", "hospital", "house", "island", "jewel", "kettle", "key", "knee", "knife", "knot", "leaf", "leg", "library", "line", "lip", "lock", "map", "match", "monkey", "moon", "mouth", "muscle", "nail", "neck", "needle", "nerve", "net", "nose", "nut", "office", "orange", "oven", "parcel", "pen", "pencil", "picture", "pig", "pin", "pipe", "plane", "plate", "plow", "pocket", "pot", "potato", "prison", "pump", "rail", "rat", "receipt", "ring", "rod", "roof", "root", "sail", "school", "scissors", "screw", "seed", "sheep", "shelf", "ship", "shirt", "shoe", "skin", "skirt", "snake", "sock", "spade", "sponge", "spoon", "spring", "square", "stamp", "star", "station", "stem", "stick", "stocking", "stomach", "store", "street", "sun", "table", "tail", "thread", "throat", "thumb", "ticket", "toe", "tongue", "tooth", "town", "train", "tray", "tree", "trousers", "umbrella", "wall", "watch", "wheel", "whip", "whistle", "window", "wing", "wire", "worm"]

# picturable_words_file = open('picturable_words/picturable.txt', 'r')
# file_word_list = open( "picturable_words/word_list.txt", "w")
# picturable_sentences = picturable_words_file.readlines()
# for word in picturable_sentences:
#     word = word.strip()
#     picturable_word_list.append(word)
#     file_word_list.write( '"' + str(word) + '", ' )
# print "picturable words :   ( length " , len(picturable_word_list), " )"
# file_word_list.close()
# picturable_words_file.close()



filenum_list = [1,2,3,4,5,6,7, 8, 9,10,11,12,13,14,15, 16, 17, 18,19,20,21,22,23,24, 25, 26, 27];
category_list = [ 
            # 0         1          2        3           4           5           6       7
            "Music", "Fashion", "Car", "Real Estate", "Beauty", "Travel", "Design", "Food", 
            # 8         9           10          11      12          13          14        15
            "Wedding", "Movie", "Photography", "Law", "Health", "Green", "Technology", "SEO",
             # 16           17          18          19          20      21          22
            "History", "Marketing", "Lifestyle", "University", "Dog", "Money", "Business",
            # 23            24          25          26          27              28      29          30          31
            "Fitness", "Education", "Science", "Shopping", "Entertainment", "Sports", "Cat", "Social Media", "Medical",
            # 32            33             34       35      36      37         38       39           40         41
            "Wine", "Celebrity Gossip", "DIY", "Nature", "Gaming", "Pet", "Finance", "Political", "Career", "Parenting",
            # 42            43      
            "Economics", "Other" ]; 
category_dict = {}

blog_dict = dict()
blog_dict["possession_per_blog"] = [0 for i in range(28)]
blog_dict["category"] = [ 5, 34, 12, 18, 12, 20, 43, 12, 43, 3, 18, 18, 8, 5, 31, 41, 5, 
                          23, 26, 5, 18, 43, 18, 18, 18, 18, 8 ]

stat_dict = dict()
stat_dict["pos"] = {}
stat_dict["agreement"] = {}
stat_dict["agreement_count"] = {}
stat_dict["type"] = {}
stat_dict["status"] = {}
# stat_dict["possession_per_blog"] = [0 for i in range(28)]

regular_word_dict = dict()
regular_word_dict["noun_met"] = 0
regular_word_dict["noun_actual"] = 0
noun_per_possession = 0;

# total_value_pos_dict = dict()
total_object_pos_dict = dict()

total_golden_value_pos_dict = dict()
total_golden_object_pos_dict = dict()

total_object_count = 0;
total_words = 0
no_agreement = no_type = no_status = 0
# file5 = open( "stat/total_stat.txt", "w")
file6 = open( "stat/total_object.txt", "w")
file_error = open( "stat/error.txt", "w")
file_all_word = open("stat/all_word.txt","w")
file_all_word_clean = open("stat/all_word_clean.txt","w")
# file7 = open( "stat/total_clean_sentence.txt", "w")

for round in range(0, len(filenum_list)):
# for round in range(0, 1):
    filename = 'Blog ' + str(filenum_list[round]) + '_reconciled.xml'
    # filename = 'Blog 1_reconciled.xml'
    filename_alone = filename.rsplit('.', 1)[0]
    file = open("reconcile/" + filename, 'r')
    
    sentences = str(file.readlines())
    print "blog_id: ", filenum_list[round] ,"\n"
    file_all_word.write("\n\n\nblog_id: " + str(filenum_list[round]) + "\n")
    # file7.write(str(filenum_list[round]) + "\n")
    #sentences = "Call me Ishmael. Some years ago - never mind how long precisely - having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world."
    
    tagged = nltk.sent_tokenize(sentences.strip())
    tagged = [nltk.word_tokenize(sent) for sent in tagged]
    tagged = [nltk.pos_tag(sent) for sent in tagged]
    
    i = 0
    noun_id = round_possession_num = 0
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
            if temp_indicate in dict(clean_tag):
                if ( str(dict(clean_tag)[temp_indicate])[0].isalpha() or str(dict(clean_tag)[temp_indicate]) =="-NONE-" ):
                    total_words += 1
                    file_all_word.write(temp_indicate + "\n")   
                    file_all_word_clean.write(temp_indicate + "  " + str(dict(clean_tag)[temp_indicate]).lower() + "\n")
                else:
                    file_error.write( "not word: " + str(temp_indicate) + ": " + str(dict(clean_tag)[temp_indicate]) +"\n")
                # print str(dict(clean_tag)[temp_indicate])
                if str(dict(clean_tag)[temp_indicate]).lower()[0] == "n":
                    # print "met NN", temp_indicate
                    regular_word_dict["noun_met"] += 1
            if temp_indicate == "/object":
                round_possession_num += 1
                blog_dict["possession_per_blog"][round] += 1
                total_object_count += 1
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
                # print "object_index_start: " , object_index_start, ": " , tag[object_index_start][0]
                # print "object_index_end: ", object_index_end, ": " , tag[object_index_end][0]
                # print "value_index_end: " , value_index_end
                # print "current index: " , current_index, ": " , tag[current_index][0]
                # print "id index: " , id_index, ": " , tag[id_index][0]
                object_value_count = 0
                object_value_arr = []
                object_value_decode = ""  
                # first_time_temp = True    
                while object_index_start <= object_index_end:
                    # print "object_index: " , object_index_start
                    if object_index_start < len(tag):
                        object_value_arr.append(str(tag[object_index_start][0]))
                        temp = str(tag[object_index_start][0]).lower()
                        temp_decode = temp.replace("\\xe2\\x80\\xb2", "'") # erase some weird characters
                        object_value_decode = object_value_decode + temp_decode + " "
                        object_value = object_value + str(tag[object_index_start][0]) + " "
                        object_pos = object_pos + str(tag[object_index_start][0]) + " " 
                        object_value_count += 1  
                        if temp in dict(clean_tag):
                            # print temp, "in clean_tag"
                            if str(dict(clean_tag)[temp]).lower()[0] == "n": # and first_time_temp:
                                regular_word_dict["noun_actual"] += 1 
                                # first_time_temp = False
                        else:
                            print "{" + temp + "} not in clean_tag"                       
                    object_index_start += 1

                if agreement_present:
                    agreement_value = str(tag[agreement_index][0]).lower()
                    no_agreement += 1
                if type_present:
                    type_value = str(tag[type_index][0]).lower()
                    no_type += 1
                if status_present:
                    status_value = str(tag[status_index][0]).lower()
                    no_status += 1
                id_value = str(tag[id_index][0])
                #            print "YESSSSS"
                line_no = i
                blog_id = filenum_list[round]
                
                object_value = object_value.replace(" \\", "")
                object_value = object_value.replace("\\", "")
                object_value = object_value.replace("\\ ", "")
                object_value = object_value.replace(" /'", "")
                # print "agreement: ", agreement_value
                # print "length: " , len(agreement_value)
                # print "type: ", type_value
                # print "status: ", status_value 

                object_value = object_value.strip()
                if object_value_count > 2:
                    file6.write("span " + str(object_value_count) + ": " + object_value+ "\n")
                if object_value not in total_object_pos_dict:
                    total_object_pos_dict[object_value] = {}
                    total_object_pos_dict[object_value]["count"] = 1
                    total_object_pos_dict[object_value]["pos"] = {}
                    total_object_pos_dict[object_value]["agreement"] = {}
                    total_object_pos_dict[object_value]["agreement_count"] = {}
                    total_object_pos_dict[object_value]["type"] = {}
                    total_object_pos_dict[object_value]["status"] = {}
                else:
                    total_object_pos_dict[object_value]["count"] += 1
                total_object_pos_dict[object_value]["object"] = object_value
                if object_value_count > 1:
                    for word in object_value_arr:
                        if word not in total_object_pos_dict:
                            total_object_pos_dict[word] = {}
                            total_object_pos_dict[word]["count"] = 1
                            total_object_pos_dict[word]["pos"] = {}
                            total_object_pos_dict[word]["agreement"] = {}
                            total_object_pos_dict[word]["agreement_count"] = {}
                            total_object_pos_dict[word]["type"] = {}
                            total_object_pos_dict[word]["status"] = {}
                        else:
                            total_object_pos_dict[word]["count"] += 1
                    total_object_pos_dict[object_value]["object"] = word

                if object_value.lower() in dict(clean_tag):
                    # print object_value, "in clean_tag"
                    temp_tag = str(dict(clean_tag)[object_value.lower()])
                    if temp_tag not in total_object_pos_dict[object_value]["pos"]:
                        total_object_pos_dict[object_value]["pos"][temp_tag] = 1
                    else:
                        total_object_pos_dict[object_value]["pos"][temp_tag] += 1

                    if temp_tag not in stat_dict["pos"]:
                        stat_dict["pos"][temp_tag] = 1
                    else:
                        stat_dict["pos"][temp_tag] += 1
                elif object_value_count > 1:
                    for word in object_value_arr:
                        if word.lower() in dict(clean_tag) and str(dict(clean_tag)[word.lower()]).lower()[0] == "n":
                            temp_tag = str(dict(clean_tag)[word.lower()])
                            print "[" + word + "]  in clean_tag"
                            if temp_tag not in total_object_pos_dict[word]["pos"]:
                                total_object_pos_dict[word]["pos"][temp_tag] = 1
                            else:
                                total_object_pos_dict[word]["pos"][temp_tag] += 1

                            if temp_tag not in stat_dict["pos"]:
                                stat_dict["pos"][temp_tag] = 1
                            else:
                                stat_dict["pos"][temp_tag] += 1
                            break
                # else:
                    # print "[" + object_value + "] not in clean_tag"

                if agreement_present:
                    if agreement_value not in total_object_pos_dict[object_value]["agreement"]:
                        total_object_pos_dict[object_value]["agreement"][agreement_value] = 1
                    else:
                        total_object_pos_dict[object_value]["agreement"][agreement_value] += 1
                    if len(agreement_value) not in total_object_pos_dict[object_value]["agreement_count"]:
                        total_object_pos_dict[object_value]["agreement_count"][len(agreement_value)] = 1
                    else:
                        total_object_pos_dict[object_value]["agreement_count"][len(agreement_value)] += 1
                    if agreement_value not in stat_dict["agreement"]:
                        stat_dict["agreement"][agreement_value] = 1
                    else: 
                        stat_dict["agreement"][agreement_value] += 1
                    if len(agreement_value) not in stat_dict["agreement_count"]:
                        stat_dict["agreement_count"][len(agreement_value)] = 1
                    else: 
                        stat_dict["agreement_count"][len(agreement_value)] += 1
                if type_present:
                    if type_value not in total_object_pos_dict[object_value]["type"]:
                        total_object_pos_dict[object_value]["type"][type_value] = 1
                    else:
                        total_object_pos_dict[object_value]["type"][type_value] += 1
                    if type_value not in stat_dict["type"]:
                        stat_dict["type"][type_value] = 1
                    else: 
                        stat_dict["type"][type_value] += 1
                if status_present:
                    if status_value not in total_object_pos_dict[object_value]["status"]:
                        total_object_pos_dict[object_value]["status"][status_value] = 1
                    else:
                        total_object_pos_dict[object_value]["status"][status_value] += 1
                    if status_value not in stat_dict["status"]:
                        stat_dict["status"][status_value] = 1
                    else: 
                        stat_dict["status"][status_value] += 1

               
                # print "\nxml_start: " , xml_start
                # print "object_index_start: " , object_index_start
                # print "object_index_end: ", object_index_end
                # print "value_index_start:", value_index_start
                # print "value_index_end: " , value_index_end
                # print "object: " , object_value
                # print "blog_id: ", blog_id
                # print to_get_clean_sentence
                file6.write( "\n" + object_value_decode + "\n" )
                file6.write( str(object_value) + "\n" )
                # print str(object_value)
                # print object_value
                            
                noun_id += 1
            j += 1


        i += 1
    tagged = str(tagged)
    if blog_dict["category"][round] not in category_dict:
        category_dict[ blog_dict["category"][round] ] = {}
        category_dict[ blog_dict["category"][round] ]["count"] = 1
        category_dict[ blog_dict["category"][round] ]["possession_num"] = round_possession_num
    else:
        category_dict[ blog_dict["category"][round] ]["count"] += 1
        category_dict[ blog_dict["category"][round] ]["possession_num"] += round_possession_num
    file.close()

noun_per_possession = regular_word_dict["noun_actual"] / float(total_object_count)



# print "\n"
file6.write("\n Stats for each object:\n")
for key, value in total_object_pos_dict.iteritems():
    # print key, ' has actual count ', total_object_pos_dict[key]["count"]
    file6.write( str(key) + " has count " + str(total_object_pos_dict[key]["count"]) + "\n" )


# print "\n"
# print "Count for noun_met:" + str(regular_word_dict["noun_met"])
file6.write("\n Count for noun_met:" + str(regular_word_dict["noun_met"])+ "\n" )
# print "\n"
# print "Count for noun_actual:" + str(regular_word_dict["noun_actual"]) 
noun_actual_div_total = float(regular_word_dict["noun_actual"] * 100 / float(regular_word_dict["noun_met"] + regular_word_dict["noun_actual"]))
file6.write("\n Count for noun_actual:" + str(regular_word_dict["noun_actual"]) + "  (" + 
    str("{0:.2f}".format(noun_actual_div_total) ) + "%)\n" )

pos_total = 0

# print "\nStats for total_pos:\n"
file6.write("\n Stats for total_pos:\n")
for key, value in stat_dict["pos"].iteritems():
    pos_total += stat_dict["pos"][key]
for key, value in stat_dict["pos"].iteritems():
    # print key, ' has count ', stat_dict["pos"][key]
    file6.write( str(key) + " has count " + str(stat_dict["pos"][key]) + "  (" + 
        str("{0:.2f}".format(stat_dict["pos"][key] * 100 / float(pos_total)) ) + "%)\n" )
# print "\n Stats for total_agreement:\n"
file6.write("\n Stats for total_agreement:\n")
for key, value in stat_dict["agreement"].iteritems():
    # print key, ' has count ', stat_dict["agreement"][key]
    file6.write( str(key) + " has count " + str(stat_dict["agreement"][key]) + "  (" + 
        str("{0:.2f}".format(stat_dict["agreement"][key] * 100 / float(no_agreement)) )+ "%)\n" )
# print "\nStats for total_agreement_count:\n"
file6.write("\n Stats for total_agreement_count:\n")
for key, value in stat_dict["agreement_count"].iteritems():
    # print key, ' has count ', stat_dict["agreement_count"][key]
    file6.write( str(key) + " has count " + str(stat_dict["agreement_count"][key]) + "  (" + 
        str("{0:.2f}".format(stat_dict["agreement_count"][key] * 100 / float(no_agreement)) ) + "%)\n" )
# print "\nStats for total_type:\n"
file6.write("\n Stats for total_type:\n")
for key, value in stat_dict["type"].iteritems():
    # print key, ' has count ', stat_dict["type"][key]
    file6.write( str(key) + " has count " + str(stat_dict["type"][key]) + "  (" + 
        str("{0:.2f}".format(stat_dict["type"][key] * 100 / float(no_type)) ) + "%)\n" )
# print "\nStats for total_status:\n"
file6.write("\n Stats for total_status:\n")
for key, value in stat_dict["status"].iteritems():
    # print key, ' has count ', stat_dict["status"][key]
    file6.write( str(key) + " has count " + str(stat_dict["status"][key]) + "  (" + 
        str("{0:.2f}".format(stat_dict["status"][key] * 100 / float(no_status)) ) + "%)\n" )

for i in range(0,27):
    file6.write("possession_per_blog for blog " + str(i+1) + ": " + str(blog_dict["possession_per_blog"][i]) )
    file6.write(", category: " + str(blog_dict["category"][i]) + "\n")


for key, value in category_dict.iteritems():
    file6.write("category " + str(category_list[key]) + ": \n    num of blogs: " + str( category_dict[key]["count"] ))
    file6.write(",    total possession_num: " + str(category_dict[key]["possession_num"]) + ",    avg possesion per blog: " +
     str("{0:.2f}".format( category_dict[key]["possession_num"] / float(category_dict[key]["count"]) ) )+ "\n")

# print "object total count: ", total_object_count
file6.write("\nobject total count: " + str(total_object_count))
file6.write("\n noun_per_possession: " + str(noun_per_possession) + "\n")
# print "object total no_agreement: ", no_agreement
file6.write("\nobject total no_agreement: " + str(no_agreement))
# print "object total no_type: ", no_type
file6.write("\nobject total no_type: " + str(no_type))
# print "object total no_status: ", no_status
file6.write("\nobject total no_status: " + str(no_status))

# print "object total words: ", total_words
file6.write("\nobject total total_words: " + str(total_words))

# file5.close()
file6.close()
# file7.close()
file_error.close()
file_all_word.close()
file_all_word_clean.close()


































