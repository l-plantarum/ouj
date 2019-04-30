#coding: UTF-8
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.local


trainings = []
for qa in db.test20190429.find(): 
    wordlist = []
    for line in qa['words']:
        wordlist.extend(line)
    training = TaggedDocument(words = wordlist, tags = [str(qa['_id'])])
    trainings.append(training)

m = Doc2Vec(documents = trainings, dm = 1, vector_size = 64, window = 8, min_count=10, workers=4)
m.save("20190429.model")
