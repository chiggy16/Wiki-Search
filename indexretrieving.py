#  retrieving the index

from collections import defaultdict
import time
import re
from Stemmer import Stemmer
import sys

name = ["title", "body", "infobox",
        "category", "external", "ref"]

a = time.time()
f = open(sys.argv[1], "r")
contents = f.read()
tokens = re.split(r'[%]', contents)
di_back = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
final = []
for j in tokens:
    final.append(re.split(r'[|]', j))
# print(final[0][0])

for i in range(0, 6):
    for j in range(0, len(final[i])):
        tatt = re.split(r'[ ]', final[i][j])
        leng = len(tatt)
        k = 1
        while(k < leng - 1):
            di_back[name[i]][tatt[0]][int(tatt[k])] = int(
                tatt[k + 1])
            k += 2
# print(time.time() - a)

idi = defaultdict(str)
f = open("id.txt", "r")
contents = f.read()
tokens = re.split(r'[|]', contents)
data_len = len(tokens)
for i in range(0, len(tokens) - 1):
    j = re.split(r'[/]', tokens[i])
    idi[int(j[0])] = j[1]

# for query in queries:
#     if query=='' or len
#     query=re.split("\n",query)


def search(word, t):
    ans = []
    stemmer = Stemmer("porter")
    word = word.lower()
    word = stemmer.stemWord(word)
#     print(t)
    if t in name:
        zz = di_back[t][word]
        for a, b in zz.items():
            ans.append((a, b))
        return ans
    for n in name:
        zz = di_back[n][word]
        for a, b in zz.items():
            ans.append((a, b))
    return ans


def merge(list1, list2):
    listans = []
    n1 = len(list1)
    n2 = len(list2)
    i = 0
    j = 0
#     print(list2)
    while(i < n1 and j < n2):
        if(int(list1[i][0]) == int(list2[j][0])):
            listans.append(list2[j])
            i += 1
            j += 1
        elif(int(list1[i][0]) < int(list2[j][0])):
            i += 1
        else:
            j += 1
    if(len(listans) == 0):
        return list1
    return listans


contents = sys.argv[2]
tokens = re.split(r'[\n]', contents)
t = ""
for i in tokens:
    j = re.split(r'[:]', i)
    if(len(j) == 1):
        j = re.split(r'[ ]', i)
        list = []
        for ll in range(0, data_len):
            list.append((ll, 0))

        for k in j:
            list = merge(list, search(k, "FSf"))
        list.sort(reverse=True)
        for k in list[0:20]:
            print(idi[k[0]])
        print("\n")
        continue
    j = re.split(r'[ ]', i)
    lene = len(j)
    list = []
    for ll in range(0, data_len):
        list.append((ll, 0))
    for k in range(0, lene):
        sp = re.split(r'[:]', j[k])
#         print(sp[0],sp[1])
        list = merge(list, search(sp[0], sp[1]))
    list.sort(reverse=True)
    for k in list[0:10]:
        print(idi[k[0]])
    print("\n")
