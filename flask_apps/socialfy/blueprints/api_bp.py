from flask import Blueprint, jsonify, redirect, request, make_response
from lib.session import require_login, users, auths
from jsonschema import validate
from lib.user import user
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
        #TODO: Replace Null Image with a served one 
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
@api.route("/secure/user/other", methods=["GET", "POST"])
@require_login
def get_friend(context):
    '''
    Gets the Users Profile Image, Display Name, Last Played Song, Url 
    '''
   
    try:
        #JSON Dictionary Schema 
        schema = {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    },
                    "required": ["user_id"],
                    }
        query = request.json
        validate(instance=query, schema=schema)
        # Create a client with Users Token
        client = tk.Spotify(context)
        # Get the Public User
        user = client.user(query["user_id"])
        # Get the Public Users Profile Photo if Present
        image = user.images
        if (len(image) == 0): 
            #TODO: Replace Null Image with a served one 
            image = "null"
        else:
            image = image[0].url      
        #Output 
        profile = {
        "display_name": user.display_name,
        "profile_photo" : image,
        "spotify_url": user.external_urls[0]
            } 
        return jsonify(profile), 200
    except:
        #Return Error if any validation fails
        return "Failure", 400

#TODO: Get Friends 
@api.route("/secure/user/friends")
@require_login
def get_friends(context):
    '''
    Gets the Friend Dictionary, Including total number of friends and a list of the user ids 
    Returns Empty List if User doesnt exist or they have no friends
    '''
    return jsonify({"friends":user(context).get_friends()}), 400

@api.route("/secure/user/friends/add")
@require_login
def add_friends(context):
    try:
        schema = {
                "type": "object",
                "properties": {
                    "display_name": {"type": "string"},
                    },
                    "required": ["display_name"],
                    } 
        query = request.json
        validate(instance=query, schema=schema)
        # Add The Friend
        status = user(context).add_friend(query["display_name"])
        if status == 0 or status == 2:
            return "Success", 200
        return "Failure", 400 
    except: 
        return "Failure", 400

@api.route("/secure/user/friends/remove")
@require_login
def remove_friend(context):
    try: 
        query = request.json
        status = user(context).remove_friend(query["friend_id"])
        if status == 0 or status == 2:
            return make_response(200)
        return make_response(400) 
    except: 
        return 400




'''
Posting Endpoints
'''


#TODO:Make Post Endpoint
@api.route("/secure/post/make", methods=["POST"])
@require_login
def make_post(context):
    '''
    Make a post of a chosen song
    '''
    try: 
        post = Post(context)
        query = request.json
        if post.create_post(song=query["song_id"], blurb=query["text_blurb"]):
            return "Success", 200
        return "Failure", 500

    except:
        return "Failure", 500

#TODO:Delete Post Endpoint 
@api.route("/secure/post/delete", methods=["POST"])
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
            return "Success", 200
        return "Failure", 500
    except:
        return "Failure", 500
    
#TODO: Like Post Endpoint
@api.route('/secure/post/like')
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
@api.route("/secure/post/add")
def add_recomendation(context):
    '''Add a post to your library (probably just to a playlist called socialfy)'''
    pass

@api.route('/secure/post/comment')
@require_login
def comment_post(context):
    '''
    Comment on a post
    '''
    try: 
        post = Post(context)
        query = request.json
        if post.add_comment(post_id=query["post_id"], blurb=query["blurb"]):
            return "Success", 200
        return "Failure", 400

    except:
        return "Failure", 400

#TODO: Delete Comment 
@api.route('/secure/post/comment/delete')
@require_login
def delete_comment_post(context):
    '''
    '''
    try: 
        post = Post(context)
        query = request.json
        if post.delete_comment(cid=query["cid"]):
            return "Success", 200
        return "Failure", 400

    except:
        return "Failure", 400

'''
Feed Generation Endpoints
'''
#TODO:Generate Feed Endpoint 
api.route('/secure/feed')
@require_login
def get_feed(context):
    pass

'''
Other Endpoints 
'''
#TODO:Search for a Song or Playlist  
api.route('/secure/song/search')
@require_login
def search(context):
    pass
 
#TODO: Function to pass through api song results
api.route('/secure/song/search')
@require_login
def song(context):
    pass




