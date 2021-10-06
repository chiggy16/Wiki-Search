from xml.dom import minidom
from nltk.corpus import stopwords
from Stemmer import Stemmer
from collections import defaultdict
import time
import re
import sys


info_box = "\{\{Infobox (.*?\n)*? *?\}\}"
category = "\[ *\[ *[cC]ategory *: *(.*?) *\] *\]"
references = "== *[Rr]eferences *==(.*?\n)+?\n"
ext_links = "== *[eE]xternal [lL]inks *== *(.*?\n)+?\n"


a = time.time()
xmldoc = minidom.parse(sys.argv[1])
mediawiki = xmldoc.getElementsByTagName("mediawiki")[0]
page = mediawiki.getElementsByTagName("page")

data = []
name = ["title", "body", "infobox",
        "category", "external", "ref"]
f = open("id.txt", "w+")
k = 0
for i in page:
    dict1 = {"title": [], "body": [], "infobox": [],
             "category": [], "external": [], "ref": []}
    try:
        title = i.getElementsByTagName("title")[0].firstChild.data
    except:
        title = ""
    f.write(str(k))
    f.write("/")
    f.write(title)
    f.write("|")
    k += 1
    dict1["title"] = [title]
    try:
        text = i.getElementsByTagName("text")[0].firstChild.data
    except:
        text = ""
    infobox = re.findall(info_box, text)
    dict1["infobox"] = infobox
    categories = re.findall(category, text)
    dict1["category"] = categories
    links = re.findall(ext_links, text)
    dict1["external"] = links
    referen = re.findall(references, text)
    # print(referen)
    dict1["ref"] = referen
    re_info = re.sub(info_box, "", text)
    re_cat = re.sub(category, "", re_info)
    re_lin = re.sub(ext_links, "", re_cat)
    body_text = re.sub(references, "", re_lin)
    dict1["body"] = [body_text]
    data.append(dict1)
f.close()
# print(data[2])
# print(len(data))


sw = set(stopwords.words('english'))
# data_sw = []
name = ["title", "body", "infobox",
        "category", "external", "ref"]


def tonizer(string):
    #     print(string)
    tokens = re.split(r'[^A-Za-z0-9]+', string)
    return tokens


def cleanup(text):
    if len(text) == 0:
        return []
    lis = []
    for i in text:
        lis = lis + (tonizer(i))
    return lis


stemmer = Stemmer("porter")
length = len(data)


# print(data_sw[2])
data1 = []


def first():
    for i in range(0, int((length))):
        dict1 = {"title": [], "body": [], "infobox": [],
                 "category": [], "external": [], "ref": []}
        for j in name:
            data[i][j] = cleanup(data[i][j])
            for k in data[i][j]:
                if k not in sw:
                    k = k.lower()
                    dict1[j].append(k)
        data1.append(dict1)
    length1 = len(data1)
    for i in range(0, length1):
        for j in name:
            lle = len(data1[i][j])
            for k in range(0, lle):
                xx = data1[i][j][k]
                data1[i][j][k] = stemmer.stemWord(xx)

first()


data_final = data1
di = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

leng = len(data_final)
for i in range(0, leng):
    for j in name:
        for k in data_final[i][j]:
            if(k.isdigit() == 0 or(k.isdigit() == 1 and len(k) <= 5)):
                di[j][k][i] += 1

# print(len(di.keys()))


# print(data_final[1])
f = open(sys.argv[2], "w+")
for i, j in di.items():
    for k, l in j.items():
        f.write(k)
        f.write(" ")
        for m, n in l.items():
            f.write(str(m))
            f.write(" ")
            f.write(str(n))
            f.write(" ")
        f.write("|")
    f.write("%")
f.close()

print(time.time() - a)

# print(data_final[2])
