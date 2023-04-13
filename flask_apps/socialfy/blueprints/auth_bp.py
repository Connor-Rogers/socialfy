'''
AUTHENTICATION BLUEPRINT:
This template includes all endpoints responsible for handeling sessions, Oauth tokens within the Socialfy ecosystem
'''
import tekore as tk
from flask import Blueprint, session
from lib.session import cred, users, auths
from flask import redirect, request

auth = Blueprint("auth_bp", __name__)


@auth.route('/login', methods=['GET'])
def login():
    '''
    Assigns the Required Scopes to the user and redirects to the Spotify API login (note: A premium account is required)
    <returns> Flask redirect to the Spotify API Login, marked with the reqired credentials and scope, if the user is in
    session they are redirected to the Socialfy application
    '''
    if 'user' in session:
        return redirect('/secure/app', 307)

    scope = tk.Scope() + tk.scope.user_library_modify \
        + tk.scope.user_read_currently_playing \
        + tk.scope.user_read_private \
        + tk.scope.user_top_read \
        + tk.scope.playlist_modify_private \
        + tk.scope.playlist_read_private
    auth = tk.UserAuth(cred, scope)
    auths[auth.state] = auth
    return redirect(auth.url, 307)


@auth.route('/callback', methods=['GET'])
def login_callback():
    '''
    Handles the Oauth Token Recived from the Spotify API after login, grabs the required infromation to keep the session
    <returns> Invalid if the authentication with Spotify was unsuccessfull and redirects to the main application if success
    '''
    code = request.args.get('code', None)
    state = request.args.get('state', None)
    auth = auths.pop(state, None)
    if auth is None:
        return 'Invalid state!', 400

    token = auth.request_token(code, state)
    session['user'] = state
    users[state] = token
    return redirect('/secure/app', 307)


@auth.route('/secure/logout', methods=['GET'])
def logout():
    '''
    Logs the user out, removes them from the list of active users
    <returns> Redirect to Landing Page
    '''
    uid = session.pop('user', None)
    if uid is not None:
        users.pop(uid, None)
    return redirect('/', 307)
