from flask import Blueprint, jsonify, redirect, request
from lib.session import require_login, users, auths
from lib.user import user, get_token
from lib.posts import Post
import tekore as tk

api = Blueprint('api_bp', __name__)


#Social API Blueprint 

'''
User/Profile Endpoints
'''
@api.route('/secure/user/self', methods=['GET'])
@require_login
def get_user(context):
    '''
    Gets the Users Profile Image, Display Name, Last Played Song, Url
    '''
    client = tk.Spotify(context)
    user = client.current_user()
    image = user.images
    if (len(image) == 0): 
        image = "null"
    else:
        image = image[0].url      
    profile = {
        "username": user.display_name,
        "profile_photo" : image,
        "spotify_url": user.external_urls
    }
    return jsonify(profile)

#TODO: Get Other User Profile Information
@api.route("secure/user/other", methods=["GET", "POST"])
@require_login
def get_friend(context):
    '''
    Gets the Users Profile Image, Display Name, Last Played Song, Url 
    '''
    query = request.json
    try: 
        client = tk.Spotify(token = get_token(friend_id= query["friend_id"]))
        user = client.current_user()
        image = user.images
        if (len(image) == 0): 
            image = "null"
        
        else:
            image = image[0].url      
        
        profile = {
        "username": user.display_name,
        "profile_photo" : image,
        "spotify_url": user.external_urls
         } 
        return jsonify(profile), 200
    
    except:
        return jsonify({"error":"failure"}), 400

#TODO: Get Friends 
@api.route("secure/user/friends")
@require_login
def get_friends(context):
    '''
    Gets the Friend Dictionary, Including total number of friends and a list of the user ids 
    Returns Empty List if User doesnt exist or they have no friends
    '''
    return jsonify({"friends":user(context).get_friends()}), 400
'''
Posting Endpoints
'''
#TODO:Make Post Endpoint
@api.route("secure/post/make")
@require_login
def make_post(context):
    '''
    Make a post of a chosen song
    '''
    try: 
        post = Post(context)
        query = request.json
        if post.create_post(song=query["song_id"], blurb=query["blurb"]):
            return 200
        return 400

    except:
        return 400

#TODO:Delete Post Endpoint 
@api.route("secure/post/delete")
@require_login
def delete_post(context):
    '''
    Delete a post or generated recomendation, return null if post is not owned by user
    Deleting removes likes, commentes and post data 
    '''
    try: 
        post = Post(context)
        query = request.json
        if post.delete_post(post_id=query["post_id"]):
            return 200
        return 400
    except:
        return 400
    
#TODO: Like Post Endpoint
@api.route('secure/post/like')
@require_login
def like_post(context):
    '''
    Like/Unlike a post your allowed to see, return updated likes aswell as ur status
    '''
    try: 
        post = Post(context)
        query = request.json
        return jsonify({"status": post.like_unlike_post(post_id=query["post_id"]), "likes": post.get_post_likes(post_id=query["post_id"])}), 400
    except:
        return jsonify({"status": False, "likes": 0}), 200
#TODO: Add Post Recomendation to Spotify
@api.route("secure/post/add")
def add_recomendation(context):
    '''Add a post to your library (probably just to a playlist called socialfy)'''
    pass

@api.route('secure/post/comment')
@require_login
def comment_post(context):
    '''
    Comment on a post
    '''
    try: 
        post = Post(context)
        query = request.json
        if post.add_comment(post_id=query["post_id"], blurb=query["blurb"]):
            return 200
        return 400

    except:
        return 400

#TODO: Delete Comment 
@api.route('secure/post/comment/delete')
@require_login
def delete_comment_post(context):
    '''
    '''
    try: 
        post = Post(context)
        query = request.json
        if post.delete_comment(cid=query["cid"]):
            return 200
        return 400

    except:
        return 400

'''
Feed Generation Endpoints
'''
#TODO:Generate Feed Endpoint 
api.route('secure/feed')
@require_login
def get_feed(context):
    pass

'''
Other Endpoints 
'''
#TODO:Search for a Song or Playlist  
api.route('secure/song/search')
@require_login
def search(context):
    pass



