from lib.db import es, USER_INDEX
from lib.db import db
from elasticsearch_dsl import Search
import logging, uuid, datetime
# User Profiles, Grab User infromation from spotify, db
class user:
    '''
    '''
    def __init__(self,token) -> None:
        self.token = token
        self.datetime =  str(datetime.datetime.now(datetime.timezone.utc))
    
    def register_user(self) ->bool:
        '''
        '''
        user = {
            "id" : str(uuid.uuid4()),
            "date_time" : self.datetime,
            "user_id" : self.token,
            "friends" : []
            }
        return db.commit_document(USER_INDEX, user)
    
    def purge_user(self) ->bool:
        return db.delete_document(self.token, USER_INDEX)

    def add_friend(self, friend_id) -> int:
        '''
        '''
        try:
            s = Search(using = es, index = USER_INDEX) \
                .query("match", friend_id=friend_id)
            result = s.execute[0]
            if friend_id in result:
                return 2 
            result["friends"].append(friend_id)
            es.update(index=USER_INDEX, id=self.token, doc = result)
            return 0
        except:
            logging.warn("Unable to remove friend")
            return 1
        
    def remove_friend(self, friend_id) ->bool:
        '''
        '''
        try:
            s = Search(using_client = es, index = USER_INDEX) \
                .query("match", id=friend_id)
            result = s.execute[0]
            if friend_id not in result:
                return "not friends" 
            result["friends"].pop(friend_id)
            es.update(index=USER_INDEX, id=self.token, doc = result)
            return "removed friend"
        except:
            logging.warn("Unable to remove friend")
            return "failure"
    
    def get_friends(friend_id) -> list:
        '''
        '''
        try:
            s = Search(using_client = es, index = USER_INDEX) \
                .query("match", id = friend_id)
            return s.execute[0].get["friends"]
        except:
            logging.warn("unable to get friends")
            return []

    def get_friend_id(self) -> str:
        '''
        '''
        try:
            s = Search(using_client = es, index = USER_INDEX) \
                .query("match", user_id = self.token)
            return s.execute[0].get["id"]
        except:
            logging.warn("unable to get friends")
            return None

def get_token(friend_id) -> str:
    '''
    '''
    try:
        s = Search(using_client = es, index = USER_INDEX) \
            .query("match", id = friend_id)
        return s.execute[0].get["user_id"]
    except:
        logging.warn("unable to get friends")
        return None