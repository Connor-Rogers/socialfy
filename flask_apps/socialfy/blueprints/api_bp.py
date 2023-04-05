from flask import Blueprint, jsonify, redirect, request, make_response
from lib.session import require_login, users, auths
from jsonschema import validate
from lib.feed import feed
from lib.db import es
from lib.user import user
from lib.posts import Post
import tekore as tk

api = Blueprint('api_bp', __name__)

# Social API Blueprint

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
        # TODO: Replace Null Image with a served one
        image = "null"
    else:
        image = image[0].url
    profile = {
        "username": user.display_name,
        "profile_photo": image,
        "spotify_url": user.external_urls[0]
    }
    return jsonify(profile)


@api.route("/secure/user/other", methods=["GET", "POST"])
@require_login
def get_friend(context):
    '''
    Gets the Users Profile Image, Display Name, Last Played Song, Url 
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
            # TODO: Replace Null Image with a served one
            image = "null"
        else:
            image = image[0].url
        # Output
        profile = {
            "display_name": user.display_name,
            "profile_photo": image,
            "spotify_url": user.external_urls[0]
        }
        return jsonify(profile), 200
    except:
        # Return Error if any validation fails
        return "Failure", 400


@api.route("/secure/user/friends")
@require_login
def get_friends(context):
    '''
    Gets the Friend Dictionary, Including total number of friends and a list of the user ids 
    Returns Empty List if User doesnt exist or they have no friends
    '''
    return jsonify({"friends": user(context).get_friends()}), 400


@api.route("/secure/user/friends/add")
@require_login
def add_friends(context):
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
        status = user(context).add_friend(query["display_name"])
        if status == 0 or status == 2:
            return "Success", 200
        return "Failure", 400
    except:
        return "Failure", 400


@api.route("/secure/user/friends/remove")
@require_login
def remove_friend(context):
    schema = {
        "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                },
        "required": ["user_id"],
    }
    try:
        query = request.json
        validate(instance=query, schema=schema)
        status = user(context).remove_friend(query["user_id"])
        if status == 0 or status == 2:
            return "Sucesss", 200
        return "Failure", 400
    except:
        return "Failure", 400


'''
Posting Endpoints
'''


# TODO:Make Post Endpoint
@api.route("/secure/post/make", methods=["POST"])
@require_login
def make_post(context):
    '''
    Make a post of a chosen song
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

    except:
        return "Failure", 500

# TODO:Delete Post Endpoint
@api.route("/secure/post/delete", methods=["POST"])
@require_login
def delete_post(context):
    '''
    Delete a post or generated recomendation, return null if post is not owned by user
    Deleting removes likes, commentes and post data 
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
    except:
        return "Failure", 400

@api.route('/secure/post/like')
@require_login
def like_post(context):
    '''
    Like/Unlike a post your allowed to see, return updated likes aswell as the status
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
        return jsonify({"status": post.like_unlike_post(post_id=query["post_id"]), "likes": post.get_post_likes(post_id=query["post_id"])}), 400
    except:
        return jsonify({"status": False, "likes": 0}), 200

'''
Feed Generation Endpoints
'''
@api.route('/secure/feed/<page>')
@require_login
def get_feed(context, page):
    return jsonify(feed(context).get_feed(page)), 200


'''
Other Endpoints 
'''
# TODO:Search for a Song or Playlist
@api.route('/secure/song/search')
@require_login
def search(context):
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
        return jsonify({"status":"error", "song_uri": song_uri}),500

    except:
        return jsonify({"status":"error", "song_uri": "None"}),500
    

# TODO:Add a Song from a Post
@api.route("/secure/song/add")
def add_recomendation(context):
    '''Add a song from a post to your library (probably just to a playlist called socialfy)'''
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
        if user(context).add_song(query.get("song_uri")): 
            return jsonify({"status":"success"}), 200
        return jsonify({"status":"error"}),500

    except:
        return jsonify({"status":"error"}),500
    

