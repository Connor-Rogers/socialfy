#Rendertemplates, HTML Rendering and other Non data-backed endpoints 
from flask import Blueprint, session, redirect, render_template, send_from_directory
from lib.session import require_login
import os
main = Blueprint('main_bp', __name__)


landing_directory= os.getcwd()+ f'/../../frontend/landing/build/static'


@main.route('/')
def landing():
    ''' User will call with with thier id to store the symbol as registered'''
    path= os.getcwd()+ f'/../../frontend/landing/build'
    print(path)
    return send_from_directory(directory=path,path='index.html')

#
@main.route('/static/<folder>/<file>')
def landing_assets(folder,file):
    ''' User will call with with thier id to store the symbol as registered'''
    
    path = folder+'/'+file
    return send_from_directory(directory=landing_directory,path=path)


@main.route('/secure/app')
@require_login
def app(context):
    '''
    Serves the Socialfy Application once Verified
    '''
    path= os.getcwd()+ f'/../../frontend/landing/build'
    print(path)
    return send_from_directory(directory=path,path='index.html')

@main.route('/secure/static/<folder>/<file>')
@require_login
def app_assets(context):
    '''
    Serves the Socialfy Application once Verified
    '''
    path= os.getcwd()+ f'/../../frontend/landing/build'
    print(path)
    return send_from_directory(directory=path,path='index.html')

@main.route('/secure/api/app')
@require_login
def testing_app(context):
    return render_template("test.html")





