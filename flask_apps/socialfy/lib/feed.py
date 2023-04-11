from lib.db import es, POST_INDEX
from lib.posts import Post
from lib.recomendations import get_recomendation
from lib.user import User
from elasticsearch_dsl import Search, Q
import tekore as tk


# generate user feed
class Feed:
    '''
    Feed
    <param> token: (str) Oauth Token 
    '''
    def __init__(self, token) -> None:
        self.token = token
        self.user_id = User(token).get_friend_id()
        self.friends = User(token).get_friends()
        pass
    def get_feed(self, page)-> list:
        '''
        Gereates feed complete with a recomendation post and friend posts
        <param> page (int) page number in feed to retrive
        <returns> list(dict) Object of post, empty list if none
        '''
        def _assemble_post_(raw_post, token) -> dict:
            spotify = tk.Spotify(token)
            #strip the song_id out of the song uri and get track information
            track = spotify.track(track_id=raw_post.song_id[-22:])
            post =  {
            "id" : raw_post.id,
            "current_user" : self.user_id,
            "friend_name" : raw_post.friend_id,
            "song_name" : track.name,
            "song_arist" : track.artists[0].name,
            "song_uri": track.uri,
            "song_album_art" : track.album.images[0].url,
            "text_blurb" : raw_post.text_blurb,
            "likes" : Post(token).get_post_likes(raw_post.id) 
            } 
            return post
        
        feed = []
        recomendation =  get_recomendation(self.token)
        # Then get the posts of the users friends/self
        q = Q("match", friend_id=self.user_id) | Q("terms", friend_id=self.friends)
        s = Search(using=es, index=POST_INDEX)\
            .query(q) \
            .sort({"date_time": {"order": "desc"}})
        raw_feed = s.execute()
        #Paginiation System 
        hits = raw_feed.hits.total["value"]
        max_pages = int(raw_feed.hits.total["value"]/ 4) 
        if raw_feed.hits.total["value"] <= 4:
            max_pages += 1
        elif (4 % raw_feed.hits.total["value"]) != 0:
            max_pages += 1
        #if no posts, but a recomendation 
        if hits == 0 and recomendation is not None: 
            feed.append(recomendation)
            return feed
        #if there is only one page of results, return it only if displaying the first page.
        elif max_pages == 1 and page == 0 :
            if recomendation is not None:
                feed.append(recomendation)
            for i in range(hits):
               feed.append(_assemble_post_(raw_feed[i], token=self.token))
            return feed
        #if there are multiple pages, calculate what needs to be loaded, do not load extra. 
        elif max_pages > 1 and ((page + 1) <= max_pages): 
            if recomendation is not None:
                feed.append(recomendation)
            i = page * 4 
            while i < (page * 4 + 4):
                try: 
                    post = _assemble_post_(raw_feed[i], token=self.token)
                    feed.append(post)
                except IndexError:
                    break
                i += 1
            return feed
        else:
            return []
    
            
        



