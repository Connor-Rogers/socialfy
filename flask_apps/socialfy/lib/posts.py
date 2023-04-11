import uuid, datetime
from lib.db import DB, POST_INDEX, LIKE_INDEX, es
from lib.user import User
import tekore as tk 
from elasticsearch_dsl import Search
#create, destroy, comment/like posts


class Post:
    """
    A class representing a post on Socialfy

    Attributes:
    -----------
    token : str
        The access token of the user creating or interacting with the post.

    datetime : str
        A string representing the current UTC datetime in ISO 8601 format.

    Methods:
    --------
    create_post(song:str, blurb:str) -> bool:
        Creates a new post with the provided song and blurb.

    delete_post(post_id:str) -> bool:
        Deletes the post with the provided ID, if the user is the owner of the post.

    like_unlike_post(post_id:str) -> bool:
        Adds or removes a "like" for the post from the current user.

    get_post_likes(post_id:str) -> int:
        Returns the total number of likes for the post with the provided ID.

    search_song(query:str) -> dict:
        Searches for a song on Spotify using the provided query string and returns a dictionary containing
        the song's name, artist, and Spotify URI.
    """
    def __init__(self, token) -> None:
        self.token  = token
        self.datetime = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        return
     
    def create_post(self, song, blurb) -> bool:
        """
        Creates a new post with the provided song and blurb text.

        Parameters:
        -----------
        song : str
            The ID of the song being shared in the post.

        blurb : str
            The text description of the post.

        Returns:
        --------
        bool
            True if the post is successfully created, False otherwise.
        """
        post ={
            "id" : str(uuid.uuid4()),
            "date_time" : self.datetime,
            "friend_id" : User(self.token).get_friend_id(),
            "song_id" : song,
            "text_blurb" : blurb
            } 
        return DB.commit_document(POST_INDEX, post)  
        
    def delete_post(self, post_id) -> bool:
        """
        Deletes the post with the provided ID, but only if the user is the owner of the post.

        Parameters:
        -----------
        post_id : str
            The ID of the post to be deleted.

        Returns:
        --------
        bool
            True if the post is successfully deleted, False otherwise.
        """
        if DB.get_owner(POST_INDEX, post_id) == User(self.token).get_friend_id():
            return DB.delete_document(type=POST_INDEX, id=post_id)
        return False

    def like_unlike_post(self, post_id) -> bool:
        """
        Adds or removes a "like" for the post from the current user.

        Parameters:
        -----------
        post_id : str
            The ID of the post to like or unlike.

        Returns:
        --------
        bool
            True if the like is successfully added or removed, False otherwise.
        """
        friend_id = User(self.token).get_friend_id()
        s = Search(using=es, index=LIKE_INDEX) \
            .query("match", friend_id = friend_id) \
            .query("match", post_id= post_id)
        response = s.execute() 
        if response.hits.total["value"] <= 0:
            like = {
                "friend_id": friend_id,
                "post_id" : post_id,
                "date_time": self.datetime
            }
            if DB.commit_document(LIKE_INDEX, doc=like):
                return True 
            
        else:
            DB.delete_document(LIKE_INDEX, user=friend_id, id=post_id)
            return False

    def get_post_likes(self, post_id) -> int:
        """
        Returns the total number of likes for the post with the provided ID.

        Parameters:
        -----------
        post_id : str
            The ID of the post to get the number of likes for.

        Returns:
        --------
        int
            The total number of likes for the post.
        """
        s = Search(using=es, index=LIKE_INDEX) \
            .query("match", post_id= post_id)
        response = s.execute()
        return response.hits.total["value"]
    
    def search_song(self, query) -> dict:
        """
        Searches for a song on Spotify using the provided query string.

        Parameters:
        -----------
        query : str
            The search query to use for finding the song.

        Returns:
        --------
        dict
            A dictionary containing information about the first song matching the search query on Spotify.
            The dictionary has the following keys:
            - 'song_name': the name of the song.
            - 'song_artist': the name of the artist who performed the song.
            - 'song_uri': the Spotify URI for the song.
        """
        spotify = tk.Spotify(self.token)
        track = spotify.search(query, types=('track',), limit= 1)[0].items[0]
        response = {
            "song_name" : track.name,
            "song_artist" : track.artists[0].name,        
            "song_uri": track.uri
        }
        return response
    


