from flask import Blueprint, jsonify, url_for
from lib.session import require_login, users, auths
import tekore as tk

api = Blueprint('api_bp', __name__)


#Social API Blueprint 
#Test Endpoint
@api.route('/test')
def index():
    return "This is an example app"

#Get User Information 
@api.route('/secure/user', methods=['GET'])
@require_login
def get_user_image(context):
    client = tk.Spotify(context)
    user = client.current_user()
    profile = {
        "username": user.display_name,
        "profile_photo" : user.images[0].url 
    }
    return jsonify(profile)

#TODO:Like/Unlike Endpoint 

#TODO:Generate Feed Endpoint 

#TODO: Comment on a Post Endpoint 

