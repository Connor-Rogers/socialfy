##This is demo code but will be the foundation of authentication 
import tekore as tk
from app import spotify
from flask import Blueprint, session
from lib.session import cred, require_login, users, auths
from flask import redirect, request

auth = Blueprint("auth_bp",__name__)

in_link = '<a href="/login">login</a>'
out_link = '<a href="/secure/logout">logout</a>'
login_msg = f'You can {in_link} or {out_link}'

@auth.route('/secure', methods=['GET'])
@require_login
def main(token):
    user = session.get('user', None)
    page = f'User ID: {user}<br>{login_msg}'
    try:
        with spotify.token_as(token):
            playback = spotify.playback_currently_playing()

        item = playback.item.name if playback else None
        page += f'<br>Now playing: {item}'
    except tk.HTTPError:
        page += '<br>Error in retrieving now playing!'
    return page

@auth.route('/login', methods=['GET'])
def login():
    if 'user' in session:
        return redirect('/secure', 307)

    scope = tk.scope.user_read_currently_playing
    auth = tk.UserAuth(cred, scope)
    auths[auth.state] = auth
   
    return redirect(auth.url, 307)

@auth.route('/callback', methods=['GET'])
def login_callback():
    code = request.args.get('code', None)
    state = request.args.get('state', None)
    auth = auths.pop(state, None)
    if auth is None:
        return 'Invalid state!', 400

    token = auth.request_token(code, state)
    session['user'] = state
    users[state] = token
    return redirect('/secure', 307)

@auth.route('/secure/logout', methods=['GET'])
def logout():
    uid = session.pop('user', None)
    if uid is not None:
        users.pop(uid, None)
    return redirect('/secure', 307)