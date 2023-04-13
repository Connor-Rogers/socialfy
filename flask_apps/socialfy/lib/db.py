from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import logging
from decouple import config
import json

# Elasticsearch Instance
es = Elasticsearch([config('ES_HOST')], verify_certs=False)

POST_INDEX = "posts"
USER_INDEX = "users"
LIKE_INDEX = "likes"
SONG_INDEX = "songs"


class DB:
    '''
    Elasticsearch Document Handler Class: 
    no-arg
    '''
    def commit_document(index, doc) -> bool:
        '''
        Commit a document to an index of choice
        <param>: index (str): target index of the document
        <param>: doc dict() document in dictionary form
        <returns>: True if Success, False if Failure
        '''
        try:
            es.index(index=index, body=doc)
            return True
        except Exception as e:
            logging.exception(e)
            return False

    def delete_document(type, user=None, id=None) -> bool:
        '''
        Commit a document to an index of choice
        <param>: type (str): target type of the document
        <param>: user (str): target user requred to delete a like 
        <param>: id(str): id of user or post 
        <returns>: True if Success, False if Failure
        '''
        # if post: delete the post and the associated comments and likes
        if type == POST_INDEX:

            try:
                s = Search(using=es, index=POST_INDEX) \
                    .query("match", id=id)
                s.delete()

                s = Search(using=es, index=LIKE_INDEX) \
                    .query("match", post_id=id)
                s.delete()

                return True
            except Exception as e:
                logging.exception(e)
                return False
        # if user: deletes all documents associated with the user
        if type == USER_INDEX:
            try:
                s = Search(using=es, index=USER_INDEX) \
                    .query("match", friend_id=id)
                s.delete()

                s = Search(using=es, index=POST_INDEX) \
                    .query("match", friend_id=id)
                s.delete()

                s = Search(using=es, index=LIKE_INDEX) \
                    .query("match", friend_id=id)
                s.delete()

                s = Search(using=es, index=SONG_INDEX) \
                    .query("match", friend_id=id)
                s.delete()
                return True
            except Exception as e:
                logging.exception(e)
                return False

        # if like: delete like document associated with post and user
        if type == LIKE_INDEX:
            try:
                s = Search(using=es, index=LIKE_INDEX) \
                    .query("match", post_id=id) \
                    .query("match", friend_id=user)
                s.delete()
                return True
            except Exception as e:
                logging.exception(e)
                return False
        logging.warn("Trying to Delete an Unknown Type")

        return False

    def get_owner(type, id) -> str:
        '''
        Get the owner of a post or like 
        <param>: type (str): target type of the document
        <param>: id of the post or like
        <returns>: True if Success, False if Failure
        '''
        try:
            s = Search(using=es, index=type) \
                .query("match", id=id) \

            return s.execute()[0].friend_id
        except Exception as e:
            logging.exception(e)
            return None


def init_indices():
    '''
    Initialize the Elasticsearch Indices
    <returns> True, stack trace if false (because failure must kill the application if this fails)
    '''
    es_mappings = json.loads(config("IDXCONF"))

    for indices in es_mappings:
        es.indices.create(index=indices, ignore=400)
        logging.info("Elasicsearch Initialized")
    return True


if __name__ == "__main__":
    # Reintialize the ES instance
    init_indices()
