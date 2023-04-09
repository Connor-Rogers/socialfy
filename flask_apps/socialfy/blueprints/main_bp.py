'''
MAIN BLUEPRINT:
This template includes all endpoints responsible for serving the React Applications to the end user.
'''
from flask import Blueprint, send_from_directory
from lib.session import require_login
from lib.user import User
import os
from decouple import config


main = Blueprint('main_bp', __name__)

#React Build Paths from ENV
landing_directory= os.getcwd() + config("LANDING_DIR")  
app_directory = os.getcwd()+ config("APP_DIR") 

@main.route('/')
def landing():
    '''  
    Serves the Socialfy Landing Page
    <returns> : React File: Index.html 
    '''
    path= os.getcwd()+ f'/../../frontend/landing/build'
    print(path)
    return send_from_directory(directory=path,path='index.html')

#
@main.route('/static/<folder>/<file>')
def landing_assets(folder,file):
    '''
    Serves the Landing Page Assets
    <param> : folder:(str): Folder of the accessed path in static
    <param> : file:(str): File chosen in the accessed pack
    <returns> :  React Asset, 404 if resource is not found
    '''
    
    path = folder+'/'+file
    return send_from_directory(directory=landing_directory,path=path)

@main.route('/secure/app')
@require_login
def app(context):
    '''
    Serves the Socialfy application once authorized, also checks if user is registered with the platform.
    <param> : context:(str): Oauth Token from Spotify 
    <returns> : React File: Index.html 
    '''
    User(context).register_user()
    path= os.getcwd()+ f'/../../frontend/socialfy/build'
    return send_from_directory(directory=path,path='index.html')

@main.route('/secure/app/static/<folder>/<file>')
@require_login
def app_assets(context, folder, file):
    '''
    Serves the Socialfy application files once authorized
    <param> : context:(str): Oauth Token from Spotify 
    <param> : folder:(str): Folder of the accessed path in static
    <param> : file:(str): File chosen in the accessed pack
    <returns> : React Asset, 404 if resource is not found
    '''
    path = folder +'/'+file
    return send_from_directory(directory=app_directory,path=path)





