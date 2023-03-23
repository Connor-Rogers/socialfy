#Rendertemplates, HTML Rendering and other Non data-backed endpoints 
from flask import Blueprint, session, redirect
from lib.session import require_login
main = Blueprint('api_bp', __name__)


#TODO: Bulid Landing Page
@main.route('/')
def index():
    return redirect ("/login")

#TODO: Bulid App Page
@main.route('secure/app')
@require_login
def app():
    pass





