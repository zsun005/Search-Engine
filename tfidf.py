import math

str_to_write = ""
read_filename = "token_map_fully_merged.txt.txt"
write_filename = "token_tfidf"
doc_number = 55393
doc_size = []

def get_document_size():
    f = open("id_size.txt", "r")
    for line in f:
        temp = line.split()
        global doc_size
        doc_size.append(int(temp[1]))


def get_weight_tf(document_size, term_freq):
    # tf = float(term_freq) / float(document_size)
    # print(tf)
    tf = term_freq
    weight_tf = 0.0
    if tf > 0:
        weight_tf = 1 + math.log(tf, 10)
    # print(weight_tf)
    return weight_tf


def get_idf(document_freq):
    return math.log(float(doc_number)/float(document_freq))


def get_tfidf(weight_tf, idf):
    return weight_tf * idf


def write_tf_idf_to_file():
    with open(write_filename + str(file) + '.txt', "a") as f:
        global str_to_write
        f.write(str_to_write + '\n')
        str_to_write = ""


def get_term_and_fre(line):
    l = line.split()
    return l


def reform_frequency_list(freq_list):
    frequency_list = []
    for item in freq_list:
        temp = item.split(':')
        id = int(temp[0])
        frequency = int(temp[1])
        frequency_list.append((id, frequency))
    return frequency_list

get_document_size()
file = 1
with open(read_filename, "r") as f:
    for line in f:
        line = line[:-1]
        temp_list = get_term_and_fre(line)
        term = temp_list[0]
        if file == 1 and term[0] == 'c':
            file = 2
        if file == 2 and term[0] == 'm':
            file = 3
        str_to_write += term
        frequency_list = reform_frequency_list(temp_list[1:])
        for t in frequency_list:
            doc_id = t[0]
            frequency = t[1]
            tfidf = get_tfidf(get_weight_tf(doc_size[doc_id-1], frequency), get_idf(len(frequency_list)))
            str_to_write += " " + str(doc_id) + ":" + str(tfidf)
        write_tf_idf_to_file()

