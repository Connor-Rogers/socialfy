from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search 
import logging 
from decouple import config

#Elasticsearch Instance
es = Elasticsearch([config('ES_HOST')], verify_certs=False)
#TODO: Make these modifable from .env
POST_INDEX = "post"
COMMENT_INDEX = "comment"
USER_INDEX = "user"
LIKE_INDEX = "like"
SONG_INDEX = "song"

class db:
    '''
    '''
    def commit_document(index, doc) -> bool:
        '''
        '''
        try:
            es.index(index=index, body=doc)
            return True
        except:
            logging.critical("Elasticsearch Failed")
            return False

    def delete_document(type, user= None, id = None, cid = None) -> bool:
        '''
        '''
        #if post: delete the post and the associated comments and likes
        if type == POST_INDEX:
           
            try: 
                s = Search(using=es, index=POST_INDEX) \
                    .query("match", id=id)
                s.delete()
                
                s = Search(using=es, index=COMMENT_INDEX) \
                    .query("match", post_id=id)
                s.delete()

                s = Search(using=es, index=LIKE_INDEX) \
                    .query("match", post_id=id)
                s.delete()
                
                return True
            except:
                logging.critical("Elasticsearch Failed")
                return False
            
        #if deleting a coment delete the document that contains both a matching post id and comment_id, and user ownership of the comment
        if (type == COMMENT_INDEX) and cid:
            try:
                    s = Search(using=es, index=COMMENT_INDEX) \
                        .query("match", post_id=id) \
                        .query("match", id=cid)
                    s.delete()
                    return True
            except:
                    logging.critical("Elasticsearch Failed")
                    return False
            
        #if user: deletes all documents associated with the user
        if type == USER_INDEX:
            try:
                    s = Search(using=es, index=USER_INDEX) \
                        .query("match", friend_id=id)
                    s.delete()
                    
                    s = Search(using=es, index=POST_INDEX) \
                        .query("match", friend_id=id)
                    s.delete()
                    
                    s = Search(using=es, index=COMMENT_INDEX) \
                        .query("match", friend_id=id)
                    s.delete()

                    s = Search(using=es, index=LIKE_INDEX) \
                        .query("match", friend_id=id)
                    s.delete()

                    s = Search(using=es, index=SONG_INDEX) \
                        .query("match", friend_id=id)
                    s.delete()
                    return True
            except:
                    logging.critical("Elasticsearch Failed")
                    return False
        
        #if like: delete like document associated with post and user
        if type == LIKE_INDEX:
            try:
                    s = Search(using=es, index=LIKE_INDEX) \
                        .query("match", post_id=id) \
                        .query("match", friend_id=user) 
                    s.delete()
                    return True
            except:
                    logging.critical("Elasticsearch Failed")
                    return False
        logging.warn("Trying to Delete an Unknown Type")
        
        return False
    
    def get_owner(type, id) -> str:
        '''
        
        '''
        try:
            s = Search(using=es, index=type) \
                        .query("match", id=id) \
                     
            return s.execute[0].get("friend_id")
        except:
            logging.warn("Unable to search for user")
            return None
    
          
def init_indices():
    '''
    '''
    try:
        for indices in config("IDXCONF"):
            es.indices.create(index=indices, ignore=400)
            logging.info("Elasicsearch Initialized")
        return True
    except Exception:
        logging.critical("Elasticsearch Failed")
        return False

            



if __name__ == "__main__":
   db.init_indices()

 