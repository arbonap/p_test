# encoding: utf-8
import sys
import json
import urllib
import urllib2
import string
from pprint import pprint
import pdb
import re
import operator

reload(sys)

sys.setdefaultencoding('utf8')

ACCESS_TOKEN = 'AT7zZ2tVp3szYbTE2OgasqcBJBixFKUuCs4D3fpDzVrhoQBH4QAAAAA'
BASE_API = "https://api.pinterest.com"

NLTK_STOPWORDS = ['all', 'just', 'being', 'over', 'both', 'through', 'yourselves', 'its', 'before', 'herself', 'had', 'should', 'them', 'his', 'very', 'they', 'not', 'during', 'now',
                  'him', 'nor', 'did', 'this', 'she', 'each', 'further', 'where', 'few', 'because', 'doing', 'some', 'are', 'our', 'ourselves', 'out', 'what', 'for', 'while', 'does', 'above', 'between', 't', 'be',
                  'we', 'who', 'were', 'here', 'hers', 'by', 'on', 'about', 'of', 'against', 's', 'or', 'own', 'into', 'yourself', 'down', 'your', 'from', 'her', 'their', 'there', 'been', 'whom',
                  'too', 'themselves', 'was', 'until', 'more', 'himself', 'that', 'but', 'don', 'with', 'than', 'those', 'he', 'me', 'myself', 'tehse', 'up', 'will', 'below', 'can', 'theirs', 'my', 'and', 'then',
                  'is', 'am', 'it', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', 'agan', 'no', 'when', 'same', 'how', 'other', 'which', 'you', 'after', 'most', 'such', 'why', 'a', 'off',
                  'i', 'yours','so', 'the', 'having', 'once']


# BOARD_PATH = "/v1/boards/{}/pins/"
# board_id_1 = "785174584973334870"
# board_id_2 = "106819891100670570"
# fields = "&fields=note" #we need the note scope
endpoint = "https://api.pinterest.com/v1/boards/106819891100670570/pins/?access_token=AZzj7xGbuzXS5izXoKQ-jB1ZYphrFKUomvHO1AhDzVrhoQBH4QAAAAA&fields=note"

def is_valid_word(word):

    word = word.lower()

    valid_characters = list(string.ascii_lowercase) + ["'", "-"]

    if (len(word) < 2) or (word[0] and word[-1] not in string.ascii_lowercase)\
    or (re.search(r'\d', word)) or (re.search(r'^https?:\/\/.*[\r\n]*', word))\
    or (re.search(r'^www.+', word)):
        return False

    if word in NLTK_STOPWORDS:
        return False

    return True


def get_request(endpoint, params=None):
    #
    # if params:
    #     params.update({'access_token': ACCESS_TOKEN})
    # else:
    #     params = {'access token': ACCESS_TOKEN}
    #
    # url = "%s%s?%s%s" % (BASE_API, path, urllib.urlencode(params), fields)
    result = urllib2.urlopen(endpoint)
    response_data = result.read()
    return json.loads(response_data)

def top_n_words(board_id, top_N=0):
    json_response = get_request(endpoint, params=None)

    raw_text_list = collect_descriptions(json_response)

    top_word_dict = {}
    for string in raw_text_list:
        if is_valid_word(string):
            if string not in top_word_dict:
                top_word_dict[string] = 1
            else:
                top_word_dict[string] += 1


    print "top_word_set", set(top_word_dict.items())
    sorted_dict = sorted(top_word_dict.items(), key=operator.itemgetter(1))
    top_scoring = sorted_dict[((len(sorted_dict)-1) - top_N):-1]
    if set(top_scoring) is not None:
        return set(top_scoring)
    else:
        return set(sorted_dict)

    print "sorted_dict", sorted_dict

def strip_string(string):
    cleaned_str = string.encode('utf-8').strip().lower()
    cleaned_str = cleaned_str.strip('\xe2\x80\xa6')
    return cleaned_str

def collect_descriptions(json_response, raw_text_list=[]):
    raw_text_list = raw_text_list

    current_data = json_response
    next_page = current_data['page']['next']

    if next_page is not None:

        pin_data_list = current_data['data']

        for pin in pin_data_list:
            pin['note'] = strip_string(pin['note'])
            if pin['note'] != '':
                pin_description_words = pin['note'].split(' ')
                raw_text_list.extend(pin_description_words)

        print raw_text_list
        new_pagination = urllib2.urlopen(next_page).read()
        next_result = json.loads(new_pagination)
        next_page = next_result['page']['next']
        current_data = next_result

        collect_descriptions(current_data, raw_text_list)
        pin_data_list = current_data['data']

        print len(raw_text_list)
    return raw_text_list


def main():
    json_response = get_request(endpoint)
    raw_text_list = collect_descriptions(json_response)
    top_n_words(endpoint)


# print get_request(endpoint, params=None)
# print is_valid_word('word')


if __name__ == '__main__':
    main()
