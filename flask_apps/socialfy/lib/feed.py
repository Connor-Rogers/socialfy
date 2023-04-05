from lib.db import es, POST_INDEX, USER_INDEX
from lib.posts import Post
from lib.recomendations import get_recomendation
from lib.user import user
from elasticsearch_dsl import Search, Q
import random
import tekore as tk


# generate user feed
class feed:
    def __init__(self, token) -> None:
        self.token = token
        self.user_id = user(token).get_friend_id()
        friends = user(token).get_friends()
        if len(friends) == 0:
            friends.append("000-NoFriends")
        self.friends = friends 
        pass
    def get_feed(self, page)-> list:
        def _assemble_post_(raw_post, token) -> dict:
            spotify = tk.Spotify(token)
            #if the track information is not there, defualt to Vibez by DaBaby
            track = spotify.track(track_id=raw_post.get("song_id","0fySG6A6qLE8IvDpayb5bM"))
            post =  {
            "id" : raw_post.get("id", "None"),
            "friend_id" : raw_post.get("friend_id","None"),
            "song_name" : track.name,
            "song_arist" : track.artists[0].name,
            "song_href": track.href,
            "song_album_art" : track.album.images[0].url,
            "text_blurb" : raw_post.get("text_blurb", "None"),
            "likes" : Post(token).get_post_likes(raw_post.get("id", "None"), 0) 
            } 

            return post
        
        feed = []
        recomendation =  get_recomendation(self.token)
        # Then get the posts of the users friends/self
        
        q = Q("match", friend_id=self.user_id) | Q("terms", friend_id=self.friends)
        s = Search(using=es, index=POST_INDEX).query(q)
        raw_feed = s.execute()
        #Paginiation System 
        hits = raw_feed.hits.total["value"]
        max_pages = (raw_feed.hits.total["value"] % 4)
        # check if there is a remainder
        if raw_feed.hits.total["value"] - ((raw_feed.hits.total["value"] % 4)* 4):
           max_pages = (raw_feed.hits.total["value"] % 4)+ 1
    
        #if no posts, but a recomendation 
        if hits == 0 and recomendation is not None: 
            feed.append(recomendation)
            print(feed)
            return feed
        #if there is only one page of results, return it only if displaying the first page.
        elif max_pages == 1 and page == 0 :
            if recomendation is not None:
                feed.append(recomendation)
            for i in range(hits):
               feed.append(_assemble_post_(raw_feed[i]))
        #if there are multiple pages, calculate what needs to be loaded, do not load extra. 
        elif max_pages > 1 and page+1 <= max_pages: 
            if recomendation is not None:
                feed.append(recomendation)
            i = page * 4 
            while i > page * 4 + 4:
               post = _assemble_post_(raw_feed[i])
               if post is None:
                   return feed 
               feed.append(post)
            return feed
        else:
            return []
    
            
        



