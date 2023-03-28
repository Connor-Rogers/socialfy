from lib.db import es, USER_INDEX
from lib.db import db
from elasticsearch_dsl import Search
import logging, uuid, datetime
import tekore as tk
# User Profiles, Grab User infromation from spotify, db
class user:
    '''
    '''
    def __init__(self,token) -> None:
        self.spotify = tk.Spotify(token)
        self.datetime =  str(datetime.datetime.now(datetime.timezone.utc))
    
    
    def register_user(self) ->bool:
        '''
        '''
        s = Search(using = es, index = USER_INDEX) \
                .query("match", id=self.spotify.current_user().id)
        if s.execute().hits.total["value"] == 0:
            user = {
                "id" : self.spotify.current_user().id,
                "date_time" : self.datetime,
                "display_name": self.spotify.current_user().display_name,
                "friends" : []
                }
            return db.commit_document(USER_INDEX, user)
        return False
    def purge_user(self) ->bool:
        return db.delete_document(self.token, USER_INDEX)

    def add_friend(self, display_name) -> int:
        '''
        '''
        try:
             
            s = Search(using = es, index = USER_INDEX) \
                .query("match", display_name=display_name)
            friend_id = s.execute()[0].get("id")
            
            s = Search(using = es, index = USER_INDEX) \
                .query("match", id=self.spotify.current_user().id)
            result = s.execute()[0]
            if friend_id in result.get("friends", []):
                return 2 
            result["friends"].append(friend_id)
            es.update(index=USER_INDEX, id=self.token, doc = result)
            return 0
        except:
            logging.warn("Unable to add friend")
            return 1
        
    def remove_friend(self, friend_id) ->int:
        '''
        '''
        try:
            s = Search(using = es, index = USER_INDEX) \
                .query("match", user_id=self.spotify.current_user().id)
            result = s.execute()[0].get("friends", [])
            if friend_id not in result:
                return 2
            result["friends"].pop(friend_id)
            es.update(index=USER_INDEX, id=self.token , doc = result)
            return 0
        except:
            logging.warn("Unable to remove friend")
            return 1
    
    def get_friends(self) -> list:
        '''
        '''
        try:
            s = Search(using = es, index = USER_INDEX) \
                        .query("match", id = self.spotify.current_user().id)
        
            if s.execute().hits.total["value"] == 0:
                return []
            s.execute()[0].get["friends"]
        except:
             logging.warn("unable to get friends")
             return []

    def get_friend_id(self) -> str:
        '''
        '''
        try:
            s = Search(using = es, index = USER_INDEX) \
                .query("match", id = self.spotify.current_user().id)
            return s.execute()[0].get["id"]
        except:
            logging.warn("unable to get friends")
            return None

 