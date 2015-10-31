import sys
import nltk
import math
import time

START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
RARE_SYMBOL = '_RARE_'
RARE_WORD_MAX_FREQ = 5
LOG_PROB_OF_ZERO = -1000


# TODO: IMPLEMENT THIS FUNCTION
# Receives a list of tagged sentences and processes each sentence to generate a list of words and a list of tags.
# Each sentence is a string of space separated "WORD/TAG" tokens, with a newline character in the end.
# Remember to include start and stop symbols in yout returned lists, as defined by the constants START_SYMBOL and STOP_SYMBOL.
# brown_words (the list of words) should be a list where every element is a list of the tags of a particular sentence.
# brown_tags (the list of tags) should be a list where every element is a list of the tags of a particular sentence.
def split_wordtags(brown_train):
    brown_words = []
    brown_tags = []
    index = 0
    for sent in brown_train:
        brown_words_sentence = []
        brown_tags_sentence = []
        brown_words_sentence.insert(0,START_SYMBOL)
        brown_words_sentence.insert(0,START_SYMBOL)
        brown_tags_sentence.insert(0,START_SYMBOL)
        brown_tags_sentence.insert(0,START_SYMBOL)

        uni_sent = sent
        test1 = uni_sent.split()
        for item in test1:
            result = item.rsplit("/",1)
            word = result[0]
            tag = result[1]
            # if "/" in word or "/" in tag:
            #     print "word: ", word, ", tag: ", tag
            brown_words_sentence.append(word)
            brown_tags_sentence.append(tag)
            index += 1
        brown_words_sentence.append(STOP_SYMBOL)
        brown_tags_sentence.append(STOP_SYMBOL)

        brown_words.append(brown_words_sentence)
        brown_tags.append(brown_tags_sentence)
    # print brown_words
    # print brown_tags
    return brown_words, brown_tags


# TODO: IMPLEMENT THIS FUNCTION
# This function takes tags from the training data and calculates tag trigram probabilities.
# It returns a python dictionary where the keys are tuples that represent the tag trigram, and the values are the log probability of that trigram
def calc_trigrams(brown_tags):
    q_values = {}
    uni_count = {}
    bi_count = {}
    tri_count = {}
    line_count = 0
    i = 0
    j = 0

    for one_tag_sentence in brown_tags:
        for j in range(0,len(one_tag_sentence)):
            # print j
            if one_tag_sentence[j] in uni_count:
                uni_count[one_tag_sentence[j]] += 1
            else:
                uni_count[one_tag_sentence[j]] = 1
            if j > 0:
                item = (one_tag_sentence[j-1], one_tag_sentence[j])
                if item in bi_count:
                    bi_count[item] += 1
                else:
                    bi_count[item] = 1
            if j > 1:
                # if one_tag_sentence[j-1] == "*" and one_tag_sentence[j-2] == "*":
                #     print "**"
                item = (one_tag_sentence[j-2], one_tag_sentence[j-1], one_tag_sentence[j])
                if item in tri_count:
                    tri_count[item] += 1
                else:
                    tri_count[item] = 1
        one_tag_sentence = []
        line_count += 1

    

    for item in tri_count:
        # print item
        last_two_tup = ( item[0], item[1] )
        if item[0] == "*" and item[1] == "*":
            # print "start of sentence"
            q_values[item] = math.log( tri_count[item]*1.0 / line_count, 2 )  
        else:
            q_values[item] = math.log( tri_count[item]*1.0 /( bi_count[last_two_tup] ), 2 )  

    # print q_values
    return q_values

# This function takes output from calc_trigrams() and outputs it in the proper format
def q2_output(q_values, filename):
    outfile = open(filename, "w")
    trigrams = q_values.keys()
    trigrams.sort()  
    for trigram in trigrams:
        output = " ".join(['TRIGRAM', trigram[0], trigram[1], trigram[2], str(q_values[trigram])])
        outfile.write(output + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Takes the words from the training data and returns a set of all of the words that occur more than 5 times (use RARE_WORD_MAX_FREQ)
# brown_words is a python list where every element is a python list of the words of a particular sentence.
# Note: words that appear exactly 5 times should be considered rare!
def calc_known(brown_words):
    known_words = set([])
    word_count = {}
    for sentence in brown_words:
        for word in sentence:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
    for key, value in word_count.iteritems():
        if word_count[key] > RARE_WORD_MAX_FREQ:
            known_words.add(key)
        # else:
        #     print key
    return known_words

# TODO: IMPLEMENT THIS FUNCTION
# Takes the words from the training data and a set of words that should not be replaced for '_RARE_'
# Returns the equivalent to brown_words but replacing the unknown words by '_RARE_' (use RARE_SYMBOL constant)
def replace_rare(brown_words, known_words):
    brown_words_rare = []
    for sentence in brown_words:
        brown_words_rare_sentence = []
        for word in sentence:
            if word in known_words:
                brown_words_rare_sentence.append( word)
            else:
                brown_words_rare_sentence.append( RARE_SYMBOL)
        brown_words_rare.append(brown_words_rare_sentence)
    # print brown_words_rare
    return brown_words_rare

# This function takes the ouput from replace_rare and outputs it to a file
def q3_output(rare, filename):
    outfile = open(filename, 'w')
    for sentence in rare:
        outfile.write(' '.join(sentence[2:-1]) + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Calculates emission probabilities and creates a set of all possible tags
# The first return value is a python dictionary where each key is a tuple in which the first element is a word
# and the second is a tag, and the value is the log probability of the emission of the word given the tag
# The second return value is a set of all possible tags for this data set
def calc_emission(brown_words_rare, brown_tags):
    e_values = {}
    taglist = set([])
    word_tag_set = set([])
    word_tag_count = {}
    tag_count = {}
    for i in range(0, len(brown_words_rare)):
        for j in range( 0, len(brown_words_rare[i]) ):
            item = (brown_words_rare[i][j], brown_tags[i][j])
            taglist.add( brown_tags[i][j] )
            word_tag_set.add(item)
            if item in word_tag_count:
                word_tag_count[item] += 1
            else:
                word_tag_count[item] = 1
            if brown_tags[i][j] in tag_count:
                tag_count[brown_tags[i][j]] += 1
            else:
                tag_count[brown_tags[i][j]] = 1
    for word_tag in word_tag_set:
        tag = word_tag[1]
        e_values[word_tag] = math.log( word_tag_count[word_tag] * 1.0 / tag_count[tag] , 2 )



    return e_values, taglist

# This function takes the output from calc_emissions() and outputs it
def q4_output(e_values, filename):
    outfile = open(filename, "w")
    emissions = e_values.keys()
    emissions.sort()  
    for item in emissions:
        output = " ".join([item[0], item[1], str(e_values[item])])
        outfile.write(output + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# This function takes data to tag (brown_dev_words), a set of all possible tags (taglist), a set of all known words (known_words),
# trigram probabilities (q_values) and emission probabilities (e_values) and outputs a list where every element is a tagged sentence 
# (in the WORD/TAG format, separated by spaces and with a newline in the end, just like our input tagged data)
# brown_dev_words is a python list where every element is a python list of the words of a particular sentence.
# taglist is a set of all possible tags
# known_words is a set of all known words

# q_values is from the return of calc_trigrams(): 
# a python dictionary where the keys are tuples that represent the tag trigram, and the values are the log probability of that trigram

# e_values is from the return of calc_emissions(): 
# The first return value is a python dictionary where each key is a tuple in which the first element is a word
# and the second is a tag, and the value is the log probability of the emission of the word given the tag

# The return value is a list of tagged sentences in the format "WORD/TAG", separated by spaces. Each sentence is a string with a 
# terminal newline, not a list of tokens. Remember also that the output should not contain the "_RARE_" symbol, but rather the
# original words of the sentence!
def viterbi(brown_dev_words, taglist, known_words, q_values, e_values):
    # print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    # for tag in taglist:
    #     print tag
    tagged = []
    result_word_tag = {}
    prob_matrix = {}
    back = {}
    sentence_num = 0
    for sentence in brown_dev_words:
        prob_matrix = {}
        # print "\n\n", sentence
        # print sentence_num
        for i in range(1, len(sentence)):
        # for i in range(1, 5):
            # print "\n\n", i
            word_current = sentence[i]
            if word_current not in known_words:
                word_current = RARE_SYMBOL
            if i == 1:
                for tag_j in taglist:
                    for tag_k in taglist:
                        word_prior = sentence[i-1]
                        if word_prior not in known_words:
                            word_prior = RARE_SYMBOL
                        if (word_prior, tag_k) not in e_values or (word_current, tag_j) not in e_values:
                            # print "(", word_prior, ",", tag_k, ") or (", word_current, ",", tag_j, ") not in e_values"
                            continue
                        # print "1111111"
                        if ( START_SYMBOL, tag_k, tag_j ) not in q_values:
                            transition_prob_current = LOG_PROB_OF_ZERO
                        else:
                            transition_prob_current = q_values[( START_SYMBOL, tag_k, tag_j )]
                        if ( START_SYMBOL, START_SYMBOL, tag_k ) not in q_values:
                            transition_prob_prior = LOG_PROB_OF_ZERO
                        else:
                            transition_prob_prior = q_values[( START_SYMBOL, START_SYMBOL, tag_k )]

                        prob_matrix[( i,tag_j,tag_k )] = transition_prob_prior + transition_prob_current \
                                                + e_values[(word_prior, tag_k)] \
                                                + e_values[(word_current, tag_j)]
                        # print " START p[", i, ",", tag_j, ",", tag_k, "]: ", prob_matrix[( i,tag_j,tag_k )]

            if i > 1:
                for tag_j in taglist:
                    for tag_k in taglist:
                        if (word_current, tag_j) not in e_values:
                            continue

                        temp_prob = {}
                        temp_best = -999999999999999999999.0
                        temp_best_index = 0
                        for tag_m in taglist:
                            if ( i-1,tag_k,tag_m ) in prob_matrix:
                                if ( tag_m, tag_k, tag_j ) not in q_values:
                                    transition_prob = LOG_PROB_OF_ZERO
                                else:
                                    transition_prob = q_values[( tag_m, tag_k, tag_j )]
                                temp_prob[tag_m] = prob_matrix[( i-1,tag_k,tag_m )] + transition_prob + e_values[(word_current, tag_j)]
                                # print "new check for [", i, ",", tag_j, ",", tag_k, "]: ", prob_matrix[( i-1,tag_k,tag_m )], " + ", transition_prob, " + ", e_values[(word_current, tag_j)], " = ", temp_prob[tag_m]
                                if temp_prob[tag_m] > temp_best:
                                    temp_best = temp_prob[tag_m]
                                    temp_best_index = tag_m
                                    prob_matrix[( i,tag_j,tag_k )] = temp_best
                                    back[( i,tag_j,tag_k )] = temp_best_index
                                    # print "new temp best for [", i, ",", tag_j, ",", tag_k, "]: ", prob_matrix[( i-1,tag_k,tag_m )], " + ", transition_prob, " + ", e_values[(word_current, tag_j)], " = ", temp_best
                        
                        
                        # if temp_best > -999999999999999999999.0:
                        #     print "\np[", i, ",", tag_j, ",", tag_k, "]: ", prob_matrix[( i,tag_j,tag_k )]
                        #     print "b[", i, ",", tag_j, ",", tag_k, "]: ", temp_best_index

        word = STOP_SYMBOL
        for tag_k in taglist:
            transition_prob = 1;
            temp_prob = {}
            temp_best = -999999999999999999999.0
            temp_best_index = 0;
            for tag_m in taglist:
                if ( len(sentence)-1,tag_k,tag_m ) in prob_matrix:
                    if ( tag_m, tag_k, word ) not in q_values:
                        transition_prob = LOG_PROB_OF_ZERO
                    else:
                        transition_prob = q_values[( tag_m, tag_k, word )]
                    temp_prob[tag_m] = prob_matrix[( len(sentence)-1,tag_k,tag_m )] + transition_prob + e_values[(word, STOP_SYMBOL)]
                    if temp_prob[tag_m] > temp_best:
                        temp_best = temp_prob[tag_m]
                        temp_best_index = tag_m
                        back[( len(sentence),STOP_SYMBOL,tag_k )] = temp_best_index
                        prob_matrix[( len(sentence),STOP_SYMBOL,tag_k )] = temp_best
            # if temp_best > -999999999999999999999.0:
            #     print "\nSTOP p[", len(sentence), ",", STOP_SYMBOL, ",", tag_k, "]: ", temp_best
            #     print "STOP b[", len(sentence), ",", STOP_SYMBOL, ",", tag_k, "]: ", temp_best_index
        
        temp_best = -999999999999999999999.0
        final_best_index = 0;
        for tag_j in taglist:
            if (len(sentence), STOP_SYMBOL, tag_j) in prob_matrix and prob_matrix[(len(sentence), STOP_SYMBOL, tag_j)] > temp_best:
                temp_best = prob_matrix[(len(sentence), STOP_SYMBOL, tag_j)]
                final_best_index = tag_j
        prev_best_tag = final_best_index
        result_tag = {}
        result_tag[len(sentence)-1] = prev_best_tag
        cur_best_tag = STOP_SYMBOL
        i = len(sentence)
        while i > 1:
            temp_tag = prev_best_tag
            temp_tag = back[i, cur_best_tag, prev_best_tag ]
            cur_best_tag = prev_best_tag
            prev_best_tag = temp_tag

            result_tag[i-2] = prev_best_tag
            i -= 1
        # for i in range(0,len(sentence)):
        #     print result_tag[i]

        result_sentence = ""
        for i in range(0,len(sentence)):
            result_sentence += sentence[i] + "/" + result_tag[i] + " "
        result_sentence = result_sentence[:-1]
        result_sentence += "\n"
        sentence_num += 1
        tagged.append(result_sentence)
        # print result_sentence
        # if sentence_num > 1:
        #     break #debug
        
    return tagged

# This function takes the output of viterbi() and outputs it to file
def q5_output(tagged, filename):
    outfile = open(filename, 'w')
    for sentence in tagged:
        outfile.write(sentence)
    outfile.close()

# TODO: IMPLEMENT THIS FUNCTION
# This function uses nltk to create the taggers described in question 6
# brown_words and brown_tags is the data to be used in training
# brown_dev_words is the data that should be tagged
# The return value is a list of tagged sentences in the format "WORD/TAG", separated by spaces. Each sentence is a string with a 
# terminal newline, not a list of tokens. 
def nltk_tagger(brown_words, brown_tags, brown_dev_words):
    # Hint: use the following line to format data to what NLTK expects for training
    training = [ zip(brown_words[i],brown_tags[i]) for i in xrange(len(brown_words)) ]

    # IMPLEMENT THE REST OF THE FUNCTION HERE
    tagged = []
    default_tagger = nltk.DefaultTagger('NOUN')
    bigram_tagger = nltk.BigramTagger( training, backoff=default_tagger )
    trigram_tagger = nltk.TrigramTagger(training, backoff=bigram_tagger)

    for sentence in brown_dev_words:
        result_sentence = ""
        # print sentence
        tagged_sentence = trigram_tagger.tag(sentence)

        for i in range(0,len(sentence)):
            result_sentence += sentence[i] + "/" + tagged_sentence[i][1] + " "
        result_sentence = result_sentence[:-1]
        result_sentence += "\n"
        tagged.append(result_sentence)


    return tagged

# This function takes the output of nltk_tagger() and outputs it to file
def q6_output(tagged, filename):
    outfile = open(filename, 'w')
    for sentence in tagged:
        outfile.write(sentence)
    outfile.close()

DATA_PATH = 'data/'
OUTPUT_PATH = 'output/'

def main():
    # start timer
    time.clock()

    # open Brown training data
    infile = open(DATA_PATH + "Brown_tagged_train.txt", "r")
    brown_train = infile.readlines()
    infile.close()

    # split words and tags, and add start and stop symbols (question 1)
    brown_words, brown_tags = split_wordtags(brown_train)

    # calculate tag trigram probabilities (question 2)
    q_values = calc_trigrams(brown_tags)

    # question 2 output
    q2_output(q_values, OUTPUT_PATH + 'B2.txt')

    # calculate list of words with count > 5 (question 3)
    known_words = calc_known(brown_words)

    # get a version of brown_words with rare words replace with '_RARE_' (question 3)
    brown_words_rare = replace_rare(brown_words, known_words)

    # question 3 output
    q3_output(brown_words_rare, OUTPUT_PATH + "B3.txt")

    # calculate emission probabilities (question 4)
    e_values, taglist = calc_emission(brown_words_rare, brown_tags)

    # question 4 output
    q4_output(e_values, OUTPUT_PATH + "B4.txt")

    # delete unneceessary data
    del brown_train
    del brown_words_rare

    # open Brown development data (question 5)
    infile = open(DATA_PATH + "Brown_dev.txt", "r")
    brown_dev = infile.readlines()
    infile.close()

    # format Brown development data here
    brown_dev_words = []
    for sentence in brown_dev:
        brown_dev_words.append(sentence.split(" ")[:-1])

    # do viterbi on brown_dev_words (question 5)
    viterbi_tagged = viterbi(brown_dev_words, taglist, known_words, q_values, e_values)

    # question 5 output
    q5_output(viterbi_tagged, OUTPUT_PATH + 'B5.txt')

    # do nltk tagging here
    nltk_tagged = nltk_tagger(brown_words, brown_tags, brown_dev_words)

    # question 6 output
    q6_output(nltk_tagged, OUTPUT_PATH + 'B6.txt')

    # print total time to run Part B
    print "Part B time: " + str(time.clock()) + ' sec'

if __name__ == "__main__": main()
