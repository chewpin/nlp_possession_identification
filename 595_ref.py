import math
import nltk
import time

# Constants to be used by you when you fill the functions
START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
MINUS_INFINITY_SENTENCE_LOG_PROB = -1000

# TODO: IMPLEMENT THIS FUNCTION
# Calculates unigram, bigram, and trigram probabilities given a training corpus
# training_corpus: is a list of the sentences. Each sentence is a string with tokens separated by spaces, ending in a newline character.
# This function outputs three python dictionaries, where the keys are tuples expressing the ngram and the value is the log probability of that ngram
def calc_probabilities(training_corpus):      
    #words = [ nltk.word_tokenize(sent) for sent in sentences ]
   # for i in sentences:
#   print i
#   break
    # print "START"
    # file_temp = open("q1_temp.txt", "w")
    unigram_p = {}
    bigram_p = {}
    trigram_p = {}
    unigram_count = {}
    bigram_count = {}
    trigram_count = {}
    word_count = 0
    line_count = 0
    uni_num = 0
    bi_num = 0
    tri_num = 0
    test1 = []
    test2 = []
    test3 = []
    count = 0

    for sent in training_corpus:
        line_count += 1 

        uni_sent = "{0}{1}{2}".format(sent, ' ', STOP_SYMBOL)
        test1 = uni_sent.split()
        bi_sent = "{0}{1}{2}{3}{4}".format(START_SYMBOL, ' ', sent, ' ', STOP_SYMBOL)
        tri_sent = "{0}{1}{0}{1}{2}{1}{3}".format(START_SYMBOL, ' ', sent, STOP_SYMBOL)
        temp_bi = bi_sent.split()
        test2 = list( nltk.bigrams(temp_bi) )
        temp_tri = tri_sent.split()
        test3 = list( nltk.trigrams(temp_tri) )
        uni_num += len(test1)
        bi_num += len(test2)
        tri_num += len(test3)

        for word in test1:
            if word in unigram_count:
                unigram_count[word] += 1
            else:
                unigram_count[word] = 1
        for word in test2:
            if word in bigram_count:
                bigram_count[word] += 1
            else:
                bigram_count[word] = 1
        for word in test3:
            if word in trigram_count:
                trigram_count[word] += 1
            else:
                trigram_count[word] = 1
    # print "uni"
    for item in unigram_count:
        item = (item,)
        unigram_p[item] = math.log( unigram_count[item[0]]*1.0 / uni_num, 2 )  
        if "captain" in item:
            print item, ": ", unigram_p[item]
        if "natural" in item:
            print item, ": ", unigram_p[item]
    # print "bi"
    for item in bigram_count:
        if item[0] == "*":
            bigram_p[item] = math.log( bigram_count[item]*1.0 / line_count , 2 )  
        else:
            bigram_p[item] = math.log( bigram_count[item]*1.0 / unigram_count[item[0]] , 2 )  
        if "and" in item and ( "religion" in item or "religious" in item or "religiously" in item ) :
            print item, ": ", bigram_p[item]
        if "natural" in item and "that" in item:
            print item, ": ", bigram_p[item]
    # print "tri"
    for item in trigram_count:
        last_two_tup = ( item[0], item[1] )
        if item[0] == "*" and item[1] == "*":
            trigram_p[item] = math.log( trigram_count[item]*1.0 / line_count, 2 )  
        else:
            trigram_p[item] = math.log( trigram_count[item]*1.0 /( bigram_count[last_two_tup] ), 2 )  
        if "and" in item and "not" in item and ( "a" in item or "buy" in item or "come" in item ) :
            print item, ": ", trigram_p[item]  
        if "natural" in item and "that" in item and "he" in item :
            print item, ": ", trigram_p[item] 
    return unigram_p, bigram_p, trigram_p

# Prints the output for q1
# Each input is a python dictionary where keys are a tuple expressing the ngram, and the value is the log probability of that ngram
def q1_output(unigrams, bigrams, trigrams, filename):
    # output probabilities
    outfile = open(filename, 'w')

    unigrams_keys = unigrams.keys()
    unigrams_keys.sort()
    for unigram in unigrams_keys:
        outfile.write('UNIGRAM ' + unigram[0] + ' ' + str(unigrams[unigram]) + '\n')

    bigrams_keys = bigrams.keys()
    bigrams_keys.sort()
    for bigram in bigrams_keys:
        outfile.write('BIGRAM ' + bigram[0] + ' ' + bigram[1]  + ' ' + str(bigrams[bigram]) + '\n')

    trigrams_keys = trigrams.keys()
    trigrams_keys.sort()    
    for trigram in trigrams_keys:
        outfile.write('TRIGRAM ' + trigram[0] + ' ' + trigram[1] + ' ' + trigram[2] + ' ' + str(trigrams[trigram]) + '\n')

    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Calculates scores (log probabilities) for every sentence
# ngram_p: python dictionary of probabilities of uni-, bi- and trigrams.
# n: size of the ngram you want to use to compute probabilities
# corpus: list of sentences to score. Each sentence is a string with tokens separated by spaces, ending in a newline character.
# This function must return a python list of scores, where the first element is the score of the first sentence, etc. 
def score(ngram_p, n, corpus):
    scores = []
    prob = 1;
    log_prob = 0;
    count = 0
    break_or_not = False
    if n == 1:
        # file_uni = open("A2.uni.txt", "w")
        test1 = []
        for sentence in corpus:
            log_prob = 0;
            break_or_not = False
            uni_sent = "{0}{1}{2}".format(sentence, ' ', STOP_SYMBOL)
            test1 = uni_sent.split()
            for word in test1:
                if (word,) in ngram_p :
                    log_prob += ngram_p[(word,)]
                else:
                    # print "NEW THING " , word, " IN UNI"
                    scores.append(MINUS_INFINITY_SENTENCE_LOG_PROB)
                    break_or_not = True
            if not break_or_not:    
                scores.append(log_prob)
            # file_uni.write(str(log_prob) + "\n")
            count += 1
    elif n == 2:
        # file_bi = open("A2.bi.txt", "w")
        count = 0
        test2 = []
        for sentence in corpus:
            log_prob = 0;
            break_or_not = False
            bi_sent = "{0}{1}{2}{3}{4}".format(START_SYMBOL, ' ', sentence, ' ', STOP_SYMBOL)
            temp_bi = bi_sent.split()
            test2 = list( nltk.bigrams(temp_bi) )
            for word in test2:
                if word in ngram_p :
                    log_prob += ngram_p[word]
                else:
                    # print "NEW THING " , word, " IN BI"
                    scores.append(MINUS_INFINITY_SENTENCE_LOG_PROB)
                    break_or_not = True
            if not break_or_not:    
                scores.append(log_prob)
            # file_bi.write(str(log_prob) + "\n")
            count += 1
    elif n == 3:
        # file_tri = open("A2.tri.txt", "w")
        count = 0
        test3 = []
        for sentence in corpus:
            log_prob = 0;
            break_or_not = False
            tri_sent = "{0}{1}{0}{1}{2}{1}{3}".format(START_SYMBOL, ' ', sentence, STOP_SYMBOL)
            temp_tri = tri_sent.split()
            test3 = list( nltk.trigrams(temp_tri) )
            for word in test3:
                if word in ngram_p :
                    log_prob += ngram_p[word]
                else:
                    # print "NEW THING " , word, " IN TRI"
                    scores.append(MINUS_INFINITY_SENTENCE_LOG_PROB)
                    break_or_not = True
            if not break_or_not:    
                scores.append(log_prob)
            # file_tri.write(str(log_prob) + "\n")
            count += 1

    # for i in range(0,3):
    #     print scores[i]
    return scores

# Outputs a score to a file
# scores: list of scores
# filename: is the output file name
def score_output(scores, filename):
    outfile = open(filename, 'w')
    for score in scores:
        outfile.write(str(score) + '\n')
    outfile.close()

# TODO: IMPLEMENT THIS FUNCTION
# Calculates scores (log probabilities) for every sentence with a linearly interpolated model
# Each ngram argument is a python dictionary where the keys are tuples that express an ngram and the value is the log probability of that ngram
# Like score(), this function returns a python list of scores
def linearscore(unigrams, bigrams, trigrams, corpus):
    scores = []
    prob = 1;
    log_prob = 0;
    count = 0
    test1 = []
    for sentence in corpus:
        count = 0
        log_prob = 0;
        uni_sent = "{0}{1}{2}".format(sentence, ' ', STOP_SYMBOL)
        test1 = uni_sent.split()
        bi_sent = "{0}{1}{2}{3}{4}".format(START_SYMBOL, ' ', sentence, ' ', STOP_SYMBOL)
        temp_bi = bi_sent.split()
        test2 = list( nltk.bigrams(temp_bi) )
        tri_sent = "{0}{1}{0}{1}{2}{1}{3}".format(START_SYMBOL, ' ', sentence, STOP_SYMBOL)
        temp_tri = tri_sent.split()
        test3 = list( nltk.trigrams(temp_tri) )

        for index in range(2, len(temp_tri)):
        # for word in test3:
            # if word in trigrams :
            if ( temp_tri[index-2], temp_tri[index-1], temp_tri[index] ) in trigrams:
                # log_prob += math.log(( pow(2,trigrams[word]) + pow(2, bigrams[(word[1],word[2])]) + pow(2, unigrams[word[2]]) ) / 3, 2)
                log_prob += math.log(( pow(2,trigrams[( temp_tri[index-2], temp_tri[index-1], temp_tri[index] )]) + pow(2, bigrams[( temp_tri[index-1], temp_tri[index] )]) + pow(2, unigrams[(temp_tri[index],) ]) ) / 3, 2)
            else:
                # print "NEW THING " , word, " IN TRI"
                # log_prob = math.log(pow(2,MINUS_INFINITY_SENTENCE_LOG_PROB), 2)
                log_prob = math.log(pow(2,MINUS_INFINITY_SENTENCE_LOG_PROB), 2)
                break
        scores.append(log_prob)
        count += 1

    # for i in range(0,len(scores)):
    #     temp = scores[i]
    #     scores[i] = math.log( temp , 2)
    # print "linear score:"
    # for i in range(0,5):
    #     print scores[i]
    return scores

DATA_PATH = 'data/'
OUTPUT_PATH = 'output/'

# DO NOT MODIFY THE MAIN FUNCTION
def main():
    # start timer
    time.clock()
    # print "main 1"
    # get data
    infile = open(DATA_PATH + 'Brown_train.txt', 'r')
    corpus = infile.readlines()
    infile.close()

    # print "main 2"
    # calculate ngram probabilities (question 1)
    unigrams, bigrams, trigrams = calc_probabilities(corpus)

    # print "main 3"
    # question 1 output
    q1_output(unigrams, bigrams, trigrams, OUTPUT_PATH + 'A1.txt')

    # print "main 4"
    # score sentences (question 2)
    uniscores = score(unigrams, 1, corpus)
    biscores = score(bigrams, 2, corpus)
    triscores = score(trigrams, 3, corpus)

    # print "main 5"
    # question 2 output
    score_output(uniscores, OUTPUT_PATH + 'A2.uni.txt')
    score_output(biscores, OUTPUT_PATH + 'A2.bi.txt')
    score_output(triscores, OUTPUT_PATH + 'A2.tri.txt')

    # print "main 6"
    # linear interpolation (question 3)
    linearscores = linearscore(unigrams, bigrams, trigrams, corpus)

    # print "main 7"
    # question 3 output
    score_output(linearscores, OUTPUT_PATH + 'A3.txt')

    # print "main 8"
    # open Sample1 and Sample2 (question 5)
    infile = open(DATA_PATH + 'Sample1.txt', 'r')
    sample1 = infile.readlines()
    infile.close()
    infile = open(DATA_PATH + 'Sample2.txt', 'r')
    sample2 = infile.readlines()
    infile.close() 
    # print "main 9"

    # score the samples
    sample1scores = linearscore(unigrams, bigrams, trigrams, sample1)
    sample2scores = linearscore(unigrams, bigrams, trigrams, sample2)

    # print "main 10"
    # question 5 output
    score_output(sample1scores, OUTPUT_PATH + 'Sample1_scored.txt')
    score_output(sample2scores, OUTPUT_PATH + 'Sample2_scored.txt')

    # print total time to run Part A
    print "Part A time: " + str(time.clock()) + ' sec'

if __name__ == "__main__": main()
