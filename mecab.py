# coding=utf-8

import  MeCab
import sys
from pymongo import MongoClient

#tagger = MeCab.Tagger('-F\s%f[6] -U\s%m -E\\n')
tagger = MeCab.Tagger('-F\s%f[6] -U\s%m -E\\n')

client = MongoClient('mongodb://localhost:27017/')
db = client.local

# とりあえずちょっとだけとってみる
for qa in db.qa.find():
    lines = qa['body'].split()
    results = []
    for line in lines:
        result = tagger.parse(line)
        results.append(result.split())
    data = {
            '_id': qa['_id'],
            'url': qa['url'],
            'postdate': qa['postdate'],
            'words': results
    }
    db.test20190414.insert_one(data)
    print(qa['url'])
