import os
import json
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from bs4.element import Comment


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def porter_stem(content):
    ps = PorterStemmer()
    content = (str(content)).lower()
    words = []
    words.extend(re.findall("[a-z0-9]+", content))
    stem_words = []
    for word in words:
        stem_words.append(ps.stem(word))
    return stem_words


def beautiful_print_map(url_map):
    for key, value in url_map.items():
        print(key, value)


def write_map_to_file(map, file_name):
    f = open(file_name, "w")
    for key in sorted (map.keys()):
        f.write(key)
        for little_key in sorted (map[key].keys()):
            f.write(' ' + str(little_key) + ":" + str(map[key][little_key]))
        f.write('\n')
    f.close()


def add_token_to_map(token_list, document_id):
    '''
    Here I treat token_map as a dict where key is token, and value is another dict (key is document id, and value is the
    frequencies correspond)
    :param token_list: list of tokens [str]
    :param document_id: int, document id from index in url map
    :return: None
    '''
    for token in token_list:
        if token not in token_map.keys():
            token_map[token] = {document_id: 1}
        elif document_id in token_map[token]:
            token_map[token][document_id] += 1
        else:
            token_map[token][document_id] = 1

id_size_map = {}
id_url_map = {}
token_map = {}
file_number = 1
temp_index = 1
index = 1
for root, dirs, files in os.walk('./DEV'):
    for file in files:
        if file.endswith('.json'):
            with open(os.path.join(root, file), 'r') as json_file:
                # add url to dictionary
                json_obj = json.load(json_file)
                id_url_map[index] = json_obj['url']
                # parse html for content as a whole string
                soup = BeautifulSoup(json_obj['content'], 'html.parser')
                # find all visible text
                texts = soup.findAll(text=True)
                visible_texts = filter(tag_visible, texts)
                # Also find all titles, headers and bold font
                title = ''
                h1 = ''
                h2 = ''
                h3 = ''
                bold = ''
                strong = ''
                if soup.title != None:
                    title = soup.title.text
                if soup.h1 != None:
                    h1 = soup.h1.text
                if soup.h2 != None:
                    h2 = soup.h2.text
                if soup.h3 != None:
                    h3 = soup.h3.text
                if soup.b != None:
                    bold = soup.b.text
                if soup.strong != None:
                    strong = soup.strong.text
                important_words = ''
                important_words += ' ' + title + ' ' + h1 + ' ' + h2 + ' ' + h3 + ' ' + bold + ' ' + strong
                # format the text
                content = " ".join(t.strip() for t in visible_texts)
                content += 5 * important_words
                # porter stemming
                token_list = porter_stem(content)
                # add token to token_map
                add_token_to_map(token_list, index)
                id_size_map[index] = len(token_list)
                index += 1
                temp_index += 1
                if temp_index > 20000:
                    file_name = "token_map" + str(file_number) + ".txt"
                    write_map_to_file(token_map, file_name)
                    token_map = {}
                    temp_index = 1
                    file_number += 1
write_map_to_file(token_map, "token_map" + str(file_number) + ".txt")

f = open("id_url.txt", "w")
for key in sorted (id_url_map.keys()):
    f.write(str(key) + ' ' + id_url_map[key] + '\n')
f.close()

f = open("id_size.txt", "w")
for key in sorted (id_size_map.keys()):
    f.write(str(key) + ' ' + str(id_size_map[key]) + '\n')
f.close()
