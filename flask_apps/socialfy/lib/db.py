from elasticsearch import Elasticsearch
import elasticsearch_dsl 
import os
from decouple import config

#Elasticsearch Instance
es = Elasticsearch([config('ES_HOST')], verify_certs=False)

def init_indices():
    for indices in config("IDXCONF"):
         es.indices.create(index=indices, ignore=400)


    

if __name__ == "__main__":
   init_indices()

 