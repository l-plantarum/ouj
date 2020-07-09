# coding=utf-8

import  MeCab
import sys
from pymongo import MongoClient
import re

# URLの正規表現
urlpattern = r"^http[s]?://.*$"
reurl = re.compile(urlpattern)

#tagger = MeCab.Tagger('-F\s%f[6] -U\s%m -E\\n')
tagger = MeCab.Tagger()

client = MongoClient('mongodb://localhost:27017/')
db = client.local

i = 0
ZEN = "".join(chr(0xff01 + i) for i in range(94))
HAN = "".join(chr(0x21 + i) for i in range(94))
convtbl = str.maketrans(ZEN, HAN)
# とりあえずちょっとだけとってみる
for qa in db.qa20200113.find({"url":"https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q11184024231"}):
    lines = qa['body'].split()
    results = []
    nmorph = 0
    for line in lines:
        print(line)
        if (reurl.match(line)):
            print("continue")
            continue

        # 全角→半角
        wordinfo = tagger.parse(line.translate(convtbl))

        # 〇判定
        wordinfo = re.sub('([A-Ea-e])<>判定', '\\1判定', wordinfo)
        # 高〇
        wordinfo = re.sub("高校?[1一](年生?)?",  "高1", wordinfo)
        wordinfo = re.sub("高校?[2二](年生?)?",  "高2", wordinfo)
        wordinfo = re.sub("高校?[3三](年生?)?",  "高3", wordinfo)

        doc = wordinfo.split('\n')
        nmorph += len(doc)
        for i  in range(len(doc)):
            d = doc[i]
            print("word:{}".format(d))
            i = i + 1
        # for d in doc:
            if (d in ['EOS', '']):
                continue
            dic = d.split('\t')
            if (dic[0] in [ '/', '?', '[', ']', '(', ')', '「', '」']):
                continue
            defs = dic[1].split(',')
#            if (defs[6] == "*"):
#                print("defs[6]=*, continue:", end="")
#                print(dic)
#                continue
            if (defs[0] in ["連体詞", "副詞", "接続詞", "助詞", "助動詞", "記号", "BOS/EOS"]):
                continue
            if (defs[1] in ["非自立"]):
                continue
            if (defs[6] in ["ない", "する", "やる", "なる", "できる", "れる"]):
                continue
            if (defs[6] in ["私", "志望", "高校", "志望", "合格"]):
                continue
            elif (defs[1] == "数"):
                results.append(dic[0])
            elif (defs[6] == '*'):
                print(defs)
                results.append(defs[7])
            else:
                print(defs)
                results.append(defs[6])

    if nmorph > 20:
	    data = {
		    '_id': qa['_id'],
		    'url': qa['url'],
		    'postdate': qa['postdate'],
		    'words': results,
		    'nmorpy': nmorph,
		    'nwords': len(results)
	    }
#	    db.test20200316.insert_one(data)
	    print(data)
