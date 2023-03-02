from flask import Flask
import tekore as tk
from decouple import config

conf = tk.config_from_environment()
cred = tk.Credentials(*conf)
spotify = tk.Spotify()

auths = {}  # Ongoing authorisations: state -> UserAuth
users = {}  # User tokens: state -> token (use state as a user ID)



def app_factory() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config('SECRET_KEY')

    from blueprints import api_bp
    app.register_blueprint(api_bp)

    from blueprints import auth_bp
    app.register_blueprint(api_bp)

    from blueprints import main_bp
    app.register_blueprint(main_bp)

    return app



if __name__ == '__main__':
    application = app_factory()
    application.run('127.0.0.1', 5000)