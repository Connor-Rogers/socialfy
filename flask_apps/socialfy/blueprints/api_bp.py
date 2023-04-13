'''
API BLUEPRINT 

All functional endpoints that handle the flow and alteration of data throughout the Flask Application
'''
from flask import Blueprint, jsonify, request
from lib.session import require_login
from jsonschema import validate
import logging
from lib.feed import Feed
from lib.user import User
from lib.posts import Post
import tekore as tk

api = Blueprint('api_bp', __name__)
'''
User/Profile Endpoints
'''
@api.route('/secure/user/self', methods=['GET'])
@require_login
def get_user(context):
    '''
    Gets the Users Profile Image, Url and Display Name
    <param> context:(str) User Oauth Token
    <returns> JSON Dictionary of Username, Profile image, Spotify Url 
    '''
    try:
        client = tk.Spotify(context)
        user = client.current_user()
        image = user.images
        if (len(image) == 0):
            image = "http://127.0.0.1:5000/secure/app/static/assets/null.png"
        else:
            image = image[0].url
        profile = {
            "username": user.display_name,
            "profile_photo": image,
            "spotify_url": user.external_urls
        }
        return jsonify(profile), 200
    except Exception as e:
        logging.exception(e)
        return "Failure", 500


@api.route("/secure/user/other", methods=["GET", "POST"])
@require_login
def get_friend(context):
    '''
    Gets the Users Profile Image, Url and Display Name
    <param> context:(str) User Oauth Token
    <param> JSON Object with user_id
    <returns> JSON Dictionary of Username, Profile image, Spotify Url 
    '''
    schema = {
    "type": "object",
            "properties": {
                "user_id": {"type": "string"},
            },
    "required": ["user_id"],
}
    try:
        # JSON Dictionary Schema
        query = request.json
        validate(instance=query, schema=schema)
        # Create a client with Users Token
        client = tk.Spotify(context)
        # Get the Public User
        user = client.user(query["user_id"])
        # Get the Public Users Profile Photo if Present
        image = user.images
        if (len(image) == 0):
            image = "http://127.0.0.1:5000/secure/app/static/assets/null.png"
        else:
            image = image[0].url
        # Output
        profile = {
            "user_id": user.id,
            "display_name": user.display_name,
            "profile_photo": image,
            "spotify_url": user.href
        }
        return jsonify(profile), 200
    except Exception as e:
        #Return Error if any validation fails
        logging.exception(e)
        return "Failure", 400


@api.route("/secure/user/friends",methods=["GET", "POST"])
@require_login
def get_friends(context):
    '''
    Gets the Friend Dictionary, Including total number of friends and a list of the user ids 
    <param> context:(str) User Oauth Token
    <returns> Empty List if User doesnt exist or they have no friends
    '''
    friends_list = User(context).get_friends()
    return jsonify({"friends":friends_list}), 200


@api.route("/secure/user/friends/add",methods=["GET", "POST"])
@require_login
def add_friends(context):
    '''
    Adds a friend given their display name.
    <param> context:(str) User Oauth Token
    <param> JSON object with user_id
    <returns> Success or Failure HTTP Status 
    '''
    schema = {
        "type": "object",
                "properties": {
                    "display_name": {"type": "string"},
                },
        "required": ["display_name"],
    }
    try:
        query = request.json
        validate(instance=query, schema=schema)
        # Add The Friend
        status = User(context).add_friend(query["display_name"])
        if status == 0 or status == 2:
            return "Success", 200
        return "Failure", 400
    except Exception as e:
        logging.exception(e)
        return "Failure", 500


@api.route("/secure/user/friends/remove",methods=["GET", "POST"])
@require_login

def remove_friend(context):
    '''
    Removes a friend given their display name.
    <param> context:(str) User Oauth Token
    <param> JSON object with display_name
    <returns> Success or Failure HTTP Status 
    '''
    schema = {
        "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                },
        "required": ["user_id"],
    }
    
    query = request.json
    validate(instance=query, schema=schema)
    status = User(context).remove_friend(query["user_id"])
    if status == 0 or status == 2:
        return "Sucesss", 200
    return "Failure", 400
    #except:
    #     return "Failure", 400


'''
Posting Endpoints
'''


# TODO:Make Post Endpoint
@api.route("/secure/post/make", methods=["POST"])
@require_login
def make_post(context):
    '''
    Make a post of a chosen song
    <param> context:(str) User Oauth Token
    <param> JSON dictionary with the fields song_id and text blurb
    <returns> Success or Failure HTTP Status 
    '''
    schema = {
        "type": "object",
                "properties": {
                    "song_id": {"type": "string"},
                    "text_blurb": {"type": "string"}
                },
        "required": ["song_id", "text_blurb"],
    }
    try:
        query = request.json
        post = Post(context)
        validate(instance=query, schema=schema)
        if post.create_post(song=query["song_id"], blurb=query["text_blurb"]):
            return "Success", 200
        return "Failure", 400
    except Exception as e:
        logging.exception(e)
        return "Failure", 500

# TODO:Delete Post Endpoint
@api.route("/secure/post/delete", methods=["POST"])
@require_login
def delete_post(context):
    '''
    Delete a post or generated recomendation, return null if post is not owned by user; deleting removes likes, commentes and post data 
    <param> context:(str) User Oauth Token
    <param> JSON dictionary with the fields post_id
    <returns> Success or Failure HTTP Status
    '''
    schema = {
        "type": "object",
                "properties": {
                    "post_id": {"type": "string"},
                },
        "required": ["post_id"],
    }
    try:
        query = request.json
        post = Post(context)
        validate(instance=query, schema=schema)
        if post.delete_post(post_id=query["post_id"]):
            return "Success", 200
        return "Failure", 400
    except Exception as e:
        logging.exception(e)
        return "Failure", 500

@api.route('/secure/post/like', methods=["GET", "POST"])
@require_login
def like_post(context):
    '''
    Like/Unlike a post your allowed to see, return updated likes aswell as the status
    <param> context:(str) User Oauth Token
    <param> JSON dictionary with the fields post_id
    <returns> JSON object with users like status and like counts
    '''
    schema = {
        "type": "object",
                "properties": {
                    "post_id": {"type": "string"},
                },
        "required": ["post_id"],
    }
    try:
        query = request.json
        validate(instance=query, schema=schema)
        post = Post(context)
        return jsonify({"status": post.like_unlike_post(post_id=query["post_id"]), "likes": post.get_post_likes(post_id=query["post_id"])}), 200
    except:
        return jsonify({"status": False, "likes": 0}), 400

'''
Feed Generation Endpoints
'''
@api.route('/secure/feed/<int:page>', methods=["GET","POST"])
@require_login
def get_feed(context, page):
    '''
    Retrieves the users personal feed
    <param> context:(str) User Oauth Token
    <param> page:(int) Page of users feed requested
    <returns> JSON list(dict()) of posts in the users feed
    '''
    return jsonify(Feed(context).get_feed(page)), 200


'''
Other Endpoints 
'''
@api.route('/secure/song/search',methods=["POST"])
@require_login
def search(context):
    '''
    Allows the user to look up a song
    <param> context:(str) User Oauth Token
    <param> JSON dictionary with selected songs artist, url and song name
    '''
    schema = {
        "type": "object",
                "properties": {
                    "query": {"type": "string"},
                },
        "required": ["query"],
    }
    try:
        query = request.json
        validate(instance=query, schema=schema)
        song_uri = Post(context).search_song(query.get("query"))
        return jsonify(song_uri), 200

    except:
        return jsonify({"status":"error", "song_uri": "None"}),500
    

# TODO:Add a Song from a Post
@api.route("/secure/song/add",methods=["POST"])
@require_login
def add_recomendation(context):
    '''
    Add a song from a post to your library in a album called Socialfy.
    <param> context:(str) User Oauth Token
    <param> JSON dictionary with song uri
    <returns> HTTP Success or Failure
    '''
    
    schema = {
        "type": "object",
                "properties": {
                    "song_uri": {"type": "string"},
                },
        "required": ["song_uri"],
    }  
    try:
        query = request.json
        validate(instance=query, schema=schema)
        if User(context).add_song(query.get("song_uri")): 
            return  "Success", 200
        return "Failure", 400
    except:
         return "Failure", 500
    

