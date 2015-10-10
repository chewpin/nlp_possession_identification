


import json
import urllib2  





query_object = "spooltable"
print "\nCalling ", query_object
# request = "{}{}{}".format("http://api.walmartlabs.com/v1/search?apiKey=fxk7dy2d8ahuqxmzufm9ah4j&query=", query_object, "&numItems=1")
request = "http://api.walmartlabs.com/v1/search?apiKey=fxk7dy2d8ahuqxmzufm9ah4j&query=%s&numItems=1" % query_object
data = json.load(urllib2.urlopen(request))
print data
if data and 'items' in data:
    objects_temp = data['items'][0]
    if objects_temp:
        category_path = str(objects_temp['categoryPath'])
        groups = category_path.split('/')
        top_2_category = '/'.join(groups[:2])
        print value_value, ": ", category_path, top_2_category
        word_category[value_value] = top_2_category
        file_each_word_category.write( str(value_value) + "\n" + str(top_2_category) + "\n" )



query_object = "kitchen"
print "\nCalling ", query_object
# request = "{}{}{}".format("http://api.walmartlabs.com/v1/search?apiKey=fxk7dy2d8ahuqxmzufm9ah4j&query=", query_object, "&numItems=1")
request = "http://api.walmartlabs.com/v1/search?apiKey=fxk7dy2d8ahuqxmzufm9ah4j&query=%s&numItems=1" % query_object
data = json.load(urllib2.urlopen(request))
print data
if data and 'items' in data:
    objects_temp = data['items'][0]
    if objects_temp:
        category_path = str(objects_temp['categoryPath'])
        groups = category_path.split('/')
        top_2_category = '/'.join(groups[:2])
        print query_object, ": ", category_path, top_2_category