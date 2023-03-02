from flask import Blueprint


api = Blueprint('api_bp', __name__)


#Social API Blueprint 
#test endpoint
@api.route('/test')
def index():
    return "This is an example app"
#TODO:Like/Unlike Endpoint 

#TODO:Generate Feed Endpoint 

#TODO: Comment on a Post Endpoint 

