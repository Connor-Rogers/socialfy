from lib.db import DB, es, USER_INDEX
from elasticsearch_dsl import Search
import logging, datetime
import tekore as tk
# User Profiles, Grab User infromation from spotify, db
class User:
    """
    A class representing a user of the social media platform.

    Attributes:
    -----------
    token : str
        The access token of the user.

    Methods:
    --------
    register_user() -> bool:
        Registers the current user in the platform's database.

    purge_user() -> bool:
        Deletes the current user's account from the platform's database.

    add_friend(display_name:str) -> int:
        Sends a friend request to the user with the given display name.

    remove_friend(friend_id:str) -> int:
        Removes the friend with the given ID from the user's friend list.

    get_friends() -> list:
        Returns a list of the user's friends.

    get_friend_id() -> str:
        Returns the ID of the current user.

    add_song(song_uri:str) -> bool:
        Adds the song with the given URI to the current user's "Socialfy" playlist on Spotify.
    """
    def __init__(self,token) -> None:
        """
        Initializes a new User instance with the provided access token.
        """
        self.spotify = tk.Spotify(token)
        self.datetime = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        self.user = self.spotify.current_user()
        self.token = token
    
    
    def register_user(self) ->bool:
        """
        Registers the current user in the platform's database.

        Returns:
        --------
        bool
            True if the user is successfully registered, False otherwise.
        """
        s = Search(using = es, index = USER_INDEX) \
                .query("match", id=self.user.id)
        if s.execute().hits.total["value"] == 0:
            
            user_profile = {
                "id" :  self.user.id,
                "date_time" : self.datetime,
                "display_name": self.user.display_name,
                "friends" : []
                }
            try:
                playlists = self.spotify.playlists(user_id=self.user.id).items
                has_playlist = False
                for p in playlists:
                    if p.name == "Socialfy":
                        has_playlist = True
                        break 
                if has_playlist:
                    self.spotify.playlist_create(user_id=self.user.id, name="Socialfy", public=False, description="Your Liked Songs from Socialfy")
            except:
                logging.warn(f"unable to create playlist for user ")
            return DB.commit_document(USER_INDEX, user_profile)
        return False
        
    def purge_user(self) ->bool:
        """
        Deletes the current user's account from the platform's database.

        Returns:
        --------
        bool
            True if the user is successfully deleted, False otherwise.
        """
        return DB.delete_document(self.token, USER_INDEX)

    def add_friend(self, display_name) -> int:
        """
        Sends a friend request to the user with the given display name.

        Parameters:
        -----------
        display_name : str
            The display name of the user to send the friend request to.

        Returns:
        --------
        int
            0 if the friend request is successfully sent.
            1 if the friend request cannot be sent.
            2 if the friend is already a friend of the user.
        """
        try:
             
            s = Search(using = es, index = USER_INDEX) \
                .query("match", display_name=display_name)
            friend_id = s.execute()[0].get("id")
            
            s = Search(using = es, index = USER_INDEX) \
                .query("match", id=self.user.id)
            result = s.execute()[0]
            if friend_id in result.friends:
                return 2 
            result["friends"].append(friend_id)
            es.update(index=USER_INDEX, id=self.user.id, doc = result)
            return 0
        except:
            logging.warn("Unable to add friend")
            return 1
        
    def remove_friend(self, friend_id) ->int:
        """
        This method searches for the current user in the Elasticsearch USER_INDEX, 
        and removes the specified friend_id from the user's friend list if it exists.
        The method then updates the user's document in the Elasticsearch index with the updated friend list.

        Args:
        friend_id (str): The unique ID of the friend to be removed from the user's friend list.

        Returns:
        int: A status code indicating the outcome of the operation:
        0: Success - Friend removed successfully.
        1: Error - Unable to remove friend (Logged warning).
        2: Failure - Friend ID not found in the user's friend list.
        """
        try:
            s = Search(using = es, index = USER_INDEX) \
                .query("match", user_id=self.user.id)
            result = s.execute()[0]
            result = result.friends
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
        Get the list of friends for the current user from Elasticsearch.
        
        Returns:
            list: A list of friend objects.
        '''
        try:
            s = Search(using = es, index = USER_INDEX) \
                        .query("match", id = self.user.id)
            response = s.execute()
            if response.hits.total["value"] == 0:
                return []
            return list(response[0].friends)
        except:
             logging.warn("unable to get friends")
             return []

    def get_friend_id(self) -> str:
        '''
        Get the user ID of the current user's friend from Spotify.
        Returns:
            str: The user ID of the friend.
        '''

        try:
            return self.user.id  
        except:
            logging.warn("unable to get friend id")
            return None
    
    def add_song(self, song_uri) -> bool:
        """
        Add a song with the specified URI to the "Socialfy" playlist of the current user.
        Args:
        song_uri (str): The Spotify URI of the song to add.
        Returns:
        bool: True if the song was added successfully, False otherwise.
        """
        playlist_id = None
        playlists = self.spotify.playlists(user_id=self.user.id).items
        for p in playlists:
            if p.name == "Socialfy":
                playlist_id = p.id
                break
        if playlist_id is None:
            return False
        try:
            song_list = []
            song_list.append(song_uri)
            self.spotify.playlist_add(playlist_id= playlist_id, uris=song_list)
            return True 
        except:
            return False 
                


 