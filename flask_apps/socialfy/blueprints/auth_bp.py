##This is demo code but will be the foundation of authentication 
from flask import Flask, request, redirect, session
import tekore as tk
from flask import Blueprint
from app import users, spotify, cred, auths

auth = Blueprint("auth_bp",__name__)


in_link = '<a href="/login">login</a>'
out_link = '<a href="/logout">logout</a>'
login_msg = f'You can {in_link} or {out_link}'

@auth.route('/', methods=['GET'])
def main():
    user = session.get('user', None)
    token = users.get(user, None)

    # Return early if no login or old session
    if user is None or token is None:
        session.pop('user', None)
        return f'User ID: None<br>{login_msg}'

    page = f'User ID: {user}<br>{login_msg}'
    if token.is_expiring:
        token = cred.refresh(token)
        users[user] = token

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
        return redirect('/', 307)

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
    return redirect('/', 307)

@auth.route('/logout', methods=['GET'])
def logout():
    uid = session.pop('user', None)
    if uid is not None:
        users.pop(uid, None)
    return redirect('/', 307)