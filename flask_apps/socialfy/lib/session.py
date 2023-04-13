from functools import wraps
import tekore as tk
from flask import session, redirect
from decouple import config

conf = (config('CLIENT_ID'), config("SECRET"), config("URI"))
cred = tk.Credentials(*conf)
users = {}
auths = {}
# Authentication decorator


def require_login(f):
    @wraps(f)
    def wrapper(*args, **kws):
        user = session.get('user', None)
        token = users.get(user, None)

    # Return early if no login or old session
        if user is None or token is None:
            session.pop('user', None)
            return redirect('/login')

        if token.is_expiring:
            token = cred.refresh(token)
            users[user] = token
        return f(token, *args, **kws)
    return wrapper
