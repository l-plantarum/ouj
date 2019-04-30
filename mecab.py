# coding=utf-8

import  MeCab
import sys
from pymongo import MongoClient

#tagger = MeCab.Tagger('-F\s%f[6] -U\s%m -E\\n')
tagger = MeCab.Tagger()

client = MongoClient('mongodb://localhost:27017/')
db = client.local

# とりあえずちょっとだけとってみる
for qa in db.qa.find():
    lines = qa['body'].split()
    results = []
    for line in lines:
        wordinfo = tagger.parse(line)
        doc = wordinfo.split('\n')
        for d in doc:
            if (d == '' or d == 'EOS'):
                continue
            dic = d.split('\t')
            defs = dic[1].split(',')
            if (defs[0] in ["助詞", "助動詞", "記号", "BOS/EOS"]):
                continue
            if (defs[1] in ["非自立"]):
                continue
            if (defs[6] == '*'):
                results.append(dic[0])
            else:
                results.append(defs[6])
    data = {
            '_id': qa['_id'],
            'url': qa['url'],
            'postdate': qa['postdate'],
            'words': results
    }
    db.test20190429.insert_one(data)
