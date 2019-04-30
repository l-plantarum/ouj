# jupyterのコード編
# 

from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from pymongo import MongoClient

m = Doc2Vec.load('20190424.model')

client = MongoClient('mongodb://localhost:27017/')
db = client.local


#2019年 k-means

# 2018年のセンター当日の投稿の一覧
center2018 = []

for qa in db.test20190414.find({'postdate': {'$gt': '2018/01/13', '$lt': '2018/01/15'}}):
    center2018.append(str(qa['_id']))

# 2019年のセンター当日の投稿の一覧
center2019 = []
for qa in db.test20190414.find({'postdate': {'$gt': '2019/01/19', '$lt': '2019/01/21'}}):
    center2019.append(str(qa['_id']))

data2019 = {}
tags = []
data = []
words = []

for qa in db.test20190429.find({'postdate': {'$gt': '2019/01/19', '$lt': '2019/01/20'}}):
      id = str(qa['_id'])
        tags.append(id)
          data.append(m.docvecs[id])
            words.append('/'.join(qa['words']))

            data2019['tags'] = tags
            data2019['data'] = data
            data2019['words'] = words
            from sklearn.cluster import KMeans
            km = KMeans(n_clusters = 10).fit_predict(data2019['data'])

