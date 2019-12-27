import re
from itertools import islice
from time import time
from nltk.stem import PorterStemmer



def porter_stem(content):
    ps = PorterStemmer()
    content = (str(content)).lower()
    words = []
    words.extend(re.findall("[a-z0-9]+", content))
    for i, word in enumerate(words):
        words[i] = ps.stem(word)
    return words


def get_tf_idfs(line):
    items = line
    to_return = []
    for item in items[1:]:
        temp = item.split(":")
        to_return.append((int(temp[0]), float(temp[1])))
    return to_return


def get_query():
    query = input("******************** Qīαη Dμ Search Engine ********************\n").split()
    return porter_stem(query)



url_id = {}
with open("id_url.txt", 'r') as f:
    for line in f:
        tokens = line.split()
        url_id[tokens[0]] = tokens[1]

lookup_table1 = {'0':1, '1':17329, '2':49866, '3':62597, '4':73481, '5':81462, '6':88908, '7':95454, '8':103187, '9':110505, 'a':127894, 'b':135427}
lookup_table2 = {'c':1, 'd':9769, 'e':15631, 'f':28378, 'g':33087, 'h':38878, 'i':43827, 'j':48753, 'k':51202, 'l':55489}
lookup_table3 = {'m':1, 'n':8832, 'o':13711, 'p':16356, 'q':24446, 'r':25165, 's':31630, 't':45281, 'u':51541, 'v':54107, 'w':56632, 'x':60421, 'y':61218, 'z':62448}

while True:
    query_list = get_query()

    start = time()

    scores = {}
    for term in query_list:
        filename = ""
        line_number = 1
        if ord(term[0]) <= ord('b'):
            line_number = lookup_table1[term[0]]
            filename = "token_tfidf1.txt"
        elif ord(term[0]) <= ord('l'):
            line_number = lookup_table2[term[0]]
            filename = "token_tfidf2.txt"
        else:
            line_number = lookup_table3[term[0]]
            filename = "token_tfidf3.txt"
        #print(filename)
        with open(filename, "r") as f:
            for _ in range(line_number):
                next(f)
            for line in f:
                l = line.split()
                if l[0][0] != term[0]:
                    break
                if l[0] == term:
                    tfidfs = get_tf_idfs(l)
                    for t in tfidfs:
                        if t[0] in scores.keys():
                            scores[t[0]] += t[1]
                        else:
                            scores[t[0]] = t[1]
    sorted_scores_items = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    result_url_ids = []
    for items in sorted_scores_items:
        result_url_ids.append(items[0])
    urls = []
    for id in result_url_ids:
        result_url = url_id[str(id)]
        urls.append(result_url)
    url_set = set()
    urls_to_print = []
    for url in urls:
        if url not in url_set:
            print(url)
            urls_to_print.append(url)
            url_set.add(url)
        if len(urls_to_print) == 5:
            break

    end = time()
    #print(end - start)
