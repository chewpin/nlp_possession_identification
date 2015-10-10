
import operator

read_word_category_dict = {}


filename = 'stat/word_category_man.txt'
file = open(filename, 'r')


sentences = file.readlines()
index = 0

read_object = ""
read_category = ""
read_word_category_dict = {}
for sentence in sentences:
	sentence = sentence.rstrip('\n')

	if index % 2 == 1:
		read_category = sentence.strip()
		read_word_category_dict[read_object] = read_category
	else:
		read_object = sentence.strip()

	index += 1


# for key, value in read_word_category_dict.iteritems():
#     # file_word_category.write( str(key) + ": " + str(value) + "\n" )
#     print (key, value)

sorted_read_word_category_dict = sorted(read_word_category_dict.items(), key=operator.itemgetter(1))
for i in range(0,len(sorted_read_word_category_dict)):
    print sorted_read_word_category_dict[i][1] , ":  " , sorted_read_word_category_dict[i][0]





file.close()